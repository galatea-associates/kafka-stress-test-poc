package kafka.poc;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

import org.apache.avro.io.BinaryEncoder;
import org.apache.avro.io.DatumWriter;
import org.apache.avro.io.EncoderFactory;
import org.apache.avro.specific.SpecificDatumWriter;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.Producer;

import java.util.Properties;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
class Typetester{
    Class testType(String x){
        return java.lang.CharSequence.class;
    }
    Class testType(int x){
        return java.lang.Integer.class;
    }
    Class testType(double x){
        return java.lang.Double.class;
    }
    Class testType(Object x){
        return java.lang.Object.class;
    }
}

public final class SimpleProducer {
    private SimpleProducer() {
    }


    private static Producer producer(){
        Properties properties = new Properties();
        properties.put("bootstrap.servers", "3.8.1.159:9092");
        properties.put("acks", "1");
        properties.put("retries", 0);
        properties.put("compression.type", "gzip");
        properties.put("batch.size", 16384);
        properties.put("linger.ms", 1);
        properties.put("buffer.memory", 33554432);
        properties.put("key.serializer", "org.apache.kafka.common.serialization.ByteArraySerializer");
        properties.put("value.serializer", "org.apache.kafka.common.serialization.ByteArraySerializer");

        return new KafkaProducer(properties);
    }

    public static <T> byte[] serializeMessage(T eventMessage, org.apache.avro.Schema classSchema) throws IOException {
        
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        BinaryEncoder encoder = EncoderFactory.get().binaryEncoder(out, null);
        DatumWriter<T> writer = new SpecificDatumWriter<T>(classSchema);
        writer.write(eventMessage, encoder);
        encoder.flush();
        out.close();
        return out.toByteArray();
    }
    
    private static Map<String,List<String[]>> read_file(String csvFile){
        Map<String,List<String[]>> map =new HashMap();
        List<String[]> keyData = new ArrayList<String[]>();
        List<String[]> valData = new ArrayList<String[]>();
        String line = "";
        String cvsSplitBy = ",";

        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {

            while ((line = br.readLine()) != null) {
                // use comma as separator
                String[] data = line.split(cvsSplitBy);
                // TODO: Make more generic
                keyData.add(new String[] {data[0]});
                valData.add(new String[] {data[1], data[2], data[3], data[4], data[5], data[6], data[7]});
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        map.put("Key Data", keyData);
        map.put("Value Data", valData);
        return map;
    }

    private static List<Class> getDatatypeClasses(String[] dataArr){
        List<Class> classList = new ArrayList<Class>();
        Typetester t = new Typetester();
            for (String data : dataArr){
                classList.add(t.testType(data));
            }
        return classList;
    }

    private static Constructor<?> findConstructor(String[] data, Class classType)
            throws NoSuchMethodException, SecurityException {
        Constructor<?> newConstructor = null;
        List<Class> classList = getDatatypeClasses(data);
        switch (data.length){
            case 1:
                newConstructor = classType.getConstructor(classList.get(0));
                break;
            case 2:
                newConstructor = classType.getConstructor(classList.get(0),
                                                          classList.get(1));
            break;
                case 3:
                newConstructor = classType.getConstructor(classList.get(0),
                                                          classList.get(1),
                                                          classList.get(2));
                break;
            case 4:
                newConstructor = classType.getConstructor(classList.get(0),
                                                          classList.get(1),
                                                          classList.get(2),
                                                          classList.get(3));
                break;
            case 5:
                newConstructor = classType.getConstructor(classList.get(0),
                                                          classList.get(1),
                                                          classList.get(2),
                                                          classList.get(3),
                                                          classList.get(4));
                break;
            case 6:
                newConstructor = classType.getConstructor(classList.get(0),
                                                          classList.get(1),
                                                          classList.get(2),
                                                          classList.get(3),
                                                          classList.get(4),
                                                          classList.get(5));
                break;
            case 7:
                newConstructor = classType.getConstructor(classList.get(0),
                                                          classList.get(1),
                                                          classList.get(2),
                                                          classList.get(3),
                                                          classList.get(4),
                                                          classList.get(5),
                                                          classList.get(6));
                break;
            case 8:
                newConstructor = classType.getConstructor(classList.get(0),
                                                          classList.get(1),
                                                          classList.get(2),
                                                          classList.get(3),
                                                          classList.get(4),
                                                          classList.get(5),
                                                          classList.get(6),
                                                          classList.get(7));
                break;
            case 9:
                newConstructor = classType.getConstructor(classList.get(0),
                                                          classList.get(1),
                                                          classList.get(2),
                                                          classList.get(3),
                                                          classList.get(4),
                                                          classList.get(5),
                                                          classList.get(6),
                                                          classList.get(7),
                                                          classList.get(8));
                break;
            case 10:
                newConstructor = classType.getConstructor(classList.get(0),
                                                          classList.get(1),
                                                          classList.get(2),
                                                          classList.get(3),
                                                          classList.get(4),
                                                          classList.get(5),
                                                          classList.get(6),
                                                          classList.get(7),
                                                          classList.get(8),
                                                          classList.get(9));
                break;
            default:
                System.out.println("Could not find the right case");
        }
        return newConstructor;
    }

    private static void start_sending(Producer kafkaProducer, String topic, List<String[]> keyData, List<String[]> valData,
        Class keyClassType, Class valueClassType) {

        try {
            Constructor<?> keyConstructor = findConstructor(keyData.get(0), keyClassType);
            Constructor<?> valueConstructor = findConstructor(valData.get(0), valueClassType);

            for (int i = 0; i < keyData.size(); i++) {

                Object[] keyObjList = new Object[keyData.get(i).length];
                System.arraycopy(keyData.get(i), 0, keyObjList, 0, keyData.get(i).length);

                Object[] valObjList = new Object[valData.get(i).length];
                System.arraycopy(valData.get(i), 0, valObjList, 0, valData.get(i).length);

                Object testKeys = keyConstructor.newInstance(keyObjList);

                Object testVal =  valueConstructor.newInstance(valObjList);
                org.apache.avro.Schema keyClassSchema = (org.apache.avro.Schema) keyClassType.getMethod("getClassSchema").invoke(testKeys);
                org.apache.avro.Schema valueClassSchema = (org.apache.avro.Schema) valueClassType.getMethod("getClassSchema").invoke(testVal);

                ProducerRecord<Object, Object> record = new ProducerRecord<>(topic,
                                                                                serializeMessage(testKeys, keyClassSchema),
                                                                                serializeMessage(testVal, valueClassSchema));
                kafkaProducer.send(record);
                System.out.println("I sent a message");

            }

            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            } catch (IllegalAccessException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            } catch (IllegalArgumentException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            } catch (InvocationTargetException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            } catch (NoSuchMethodException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            } catch (SecurityException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            } catch (InstantiationException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            
        
    } 

    public static void main(String[] args) {

        Producer kafkaProducer = producer();


        String csvFile = "./out/inst-ref.csv";
        String topic = "instrument_reference_data";
        Map<String,List<String[]>> data = read_file(csvFile);
        start_sending(kafkaProducer, topic, data.get("Key Data"), data.get("Value Data"), instrument_reference_data_keys.class, instrument_reference_data_values.class);
               
        kafkaProducer.flush();
        kafkaProducer.close();
    }
}
