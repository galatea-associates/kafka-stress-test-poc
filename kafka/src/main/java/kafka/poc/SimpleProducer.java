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
import java.util.List;

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
    
    private static List<String[]> read_file(String csvFile){
        List<String[]> data = new ArrayList<String[]>();
        String line = "";
        String cvsSplitBy = ",";

        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {

            while ((line = br.readLine()) != null) {

                // use comma as separator
                data.add(line.split(cvsSplitBy));

            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        return data;
    }


    private static void start_sending(Producer kafkaProducer, String topic, List<String[]> data, Class keyClassType,
        Class valueClassType) {

        try {
            Constructor<?> keyConstructor = keyClassType.getConstructor(java.lang.CharSequence.class);
            Constructor<?> valueConstructor = valueClassType.getConstructor(java.lang.CharSequence.class,
                                                                            java.lang.CharSequence.class,
                                                                            java.lang.CharSequence.class,
                                                                            java.lang.CharSequence.class,
                                                                            java.lang.CharSequence.class,
                                                                            java.lang.CharSequence.class,
                                                                            java.lang.CharSequence.class);

            for (String[] singleData : data) {

                Object testKeys = keyConstructor.newInstance(new Object[] { singleData[0] });

                Object testVal =  valueConstructor.newInstance(new Object[] { singleData[1],
                                                                                singleData[2],
                                                                                singleData[3],
                                                                                singleData[4],
                                                                                singleData[5],
                                                                                singleData[6],
                                                                                singleData[7] });
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
        List<String[]> data = read_file(csvFile);
        start_sending(kafkaProducer, topic, data, instrument_reference_data_keys.class, instrument_reference_data_values.class);
               
        kafkaProducer.flush();
        kafkaProducer.close();
    }
}
