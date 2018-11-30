package kafka.poc;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.FileReader;
import java.io.IOException;

import kafka.poc.*;

import org.apache.avro.io.BinaryEncoder;
import org.apache.avro.io.DatumWriter;
import org.apache.avro.io.EncoderFactory;
import org.apache.avro.specific.SpecificDatumWriter;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerConfig;

import java.util.Properties;
import java.util.List;
import java.util.ArrayList;

public final class SimpleProducer {
    private SimpleProducer() {
    }
    
    public static byte[] serializeMessageValues(instrument_reference_data_values eventMessage) throws IOException {

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        BinaryEncoder encoder = EncoderFactory.get().binaryEncoder(out, null);
        DatumWriter<instrument_reference_data_values> writer = new SpecificDatumWriter<instrument_reference_data_values>(instrument_reference_data_values.getClassSchema());
        writer.write(eventMessage, encoder);
        encoder.flush();
        out.close();
        return out.toByteArray();
    }

    public static byte[] serializeMessageKeys(instrument_reference_data_keys eventMessage) throws IOException {

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        BinaryEncoder encoder = EncoderFactory.get().binaryEncoder(out, null);
        DatumWriter<instrument_reference_data_keys> writer = new SpecificDatumWriter<instrument_reference_data_keys>(instrument_reference_data_keys.getClassSchema());
        writer.write(eventMessage, encoder);
        encoder.flush();
        out.close();
        return out.toByteArray();
    }
    
    /**
     * Says hello to the world.
     * @param args The arguments of the program.
     */

    public static void main(String[] args) {

        Properties properties = new Properties();
        /*properties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "3.8.1.159:9092");
        properties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,
                  io.confluent.kafka.serializers.KafkaAvroSerializer.class);
        properties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
                  io.confluent.kafka.serializers.KafkaAvroSerializer.class);
        properties.put("schema.registry.url", "http://localhost:8081");*/
        properties.put("bootstrap.servers", "3.8.1.159:9092");
        properties.put("acks", "1");
        properties.put("retries", 0);
        properties.put("compression.type", "gzip");
        properties.put("batch.size", 16384);
        properties.put("linger.ms", 1);
        properties.put("buffer.memory", 33554432);
        properties.put("key.serializer", "org.apache.kafka.common.serialization.ByteArraySerializer");
        properties.put("value.serializer", "org.apache.kafka.common.serialization.ByteArraySerializer");

        Producer kafkaProducer = new KafkaProducer(properties);


        String csvFile = "./src/out/inst-ref.csv";
        String line = "";
        String cvsSplitBy = ",";
        List<String[]> data = new ArrayList<String[]>();

        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {

            while ((line = br.readLine()) != null) {

                // use comma as separator
                data.add(line.split(cvsSplitBy));

            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        for (String[] singleData : data) {

            instrument_reference_data_keys testKeys = instrument_reference_data_keys.newBuilder()
                                                        .setInstId(singleData[0])
                                                        .build();

            instrument_reference_data_values testVal = instrument_reference_data_values.newBuilder()
                                                        .setAssetClass(singleData[1])
                                                        .setCOI(singleData[2])
                                                        .setRIC(singleData[3])
                                                        .setISIN(singleData[4])
                                                        .setSEDOL(singleData[5])
                                                        .setTicker(singleData[6])
                                                        .setCusip(singleData[7])
                                                        .build();



            try {
                ProducerRecord<Object, Object> record = new ProducerRecord<>("instrument_reference_data", serializeMessageKeys(testKeys),
                        serializeMessageValues(testVal));
                kafkaProducer.send(record);
                System.out.println("I sent a message");
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

            
        }        
        kafkaProducer.flush();
        kafkaProducer.close();
    }
}
