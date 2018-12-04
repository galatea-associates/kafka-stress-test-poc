package kafka.poc;

import java.util.Map;

public final class PopulateAvroTopic {
    private PopulateAvroTopic() {

    }

    public static org.apache.avro.specific.SpecificRecord populateData(
            instrument_reference_data_keys instRefKeys, Map<String, String> data) {
        instRefKeys.setInstId(data.get("inst_id"));
        return instRefKeys;
    }

    public static org.apache.avro.specific.SpecificRecord populateData(
            instrument_reference_data_values instRefVals, Map<String, String> data) {
        instRefVals.setAssetClass(data.get("asset_class"));
        instRefVals.setCOI(data.get("COI"));
        instRefVals.setCusip(data.get("Cusip"));
        instRefVals.setISIN(data.get("ISIN"));
        instRefVals.setRIC(data.get("RIC"));
        instRefVals.setSEDOL(data.get("SEDOL"));
        instRefVals.setTicker(data.get("Ticker"));
        return instRefVals;
    }

    public static org.apache.avro.specific.SpecificRecord populateData(prices_keys pricesKeys,
            Map<String, String> data) {
        pricesKeys.setInstId(data.get("inst_id"));
        return pricesKeys;
    }

    public static org.apache.avro.specific.SpecificRecord populateData(prices_values pricesVals,
            Map<String, String> data) {
        pricesVals.setCurr(data.get("curr"));
        pricesVals.setPrice(Double.parseDouble(data.get("price")));
        return pricesVals;
    }

    public static org.apache.avro.specific.SpecificRecord populateData(
            position_data_keys positionKeys, Map<String, String> data) {
        positionKeys.setInstId(data.get("inst_id"));
        positionKeys.setAccount(data.get("account"));
        positionKeys.setEffectiveDate(data.get("effective_date"));
        positionKeys.setKnowledgeDate(data.get("knowledge_date"));
        positionKeys.setPurpose(data.get("purpose"));
        positionKeys.setType(data.get("type"));
        return positionKeys;
    }

    public static org.apache.avro.specific.SpecificRecord populateData(
            position_data_values positionVals, Map<String, String> data) {
        positionVals.setDirection(data.get("direction"));
        positionVals.setQty(Integer.parseInt(data.get("qty")));
        return positionVals;
    }

    public static org.apache.avro.specific.SpecificRecord[] populateData(Topic topic,
            org.apache.avro.specific.SpecificRecord[] SpecificRecord, Map<String, String> data) {
        org.apache.avro.specific.SpecificRecord updatedKey = SpecificRecord[0];
        org.apache.avro.specific.SpecificRecord updatedVal = SpecificRecord[1];
        switch (topic) {
            case INST_REF:
                updatedKey = populateData((instrument_reference_data_keys) updatedKey, data);
                updatedVal = populateData((instrument_reference_data_values) updatedVal, data);
                break;

            case PRICES:
                updatedKey = populateData((prices_keys) updatedKey, data);
                updatedVal = populateData((prices_values) updatedVal, data);
                break;

            case POSITION:
                updatedKey = populateData((position_data_keys) updatedKey, data);
                updatedVal = populateData((position_data_values) updatedVal, data);
                break;

            default:
                break;
        }
        return new org.apache.avro.specific.SpecificRecord[] {updatedKey, updatedVal};
    }


}
