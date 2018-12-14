package kafka.poc;

import org.apache.avro.specific.SpecificRecord;

import java.util.Map;

public final class PopulateAvroTopic {
    private PopulateAvroTopic() {

    }

    public static SpecificRecord populateData(
            instrument_reference_data_keys instRefKeys, Map<String, String> data) {
        instRefKeys.setInstId(data.get("inst_id"));
        return instRefKeys;
    }

    public static SpecificRecord populateData(
            instrument_reference_data_values instRefVals, Map<String, String> data) {
        instRefVals.setAssetClass(data.get("asset_class"));
        instRefVals.setCoi(data.get("coi"));
        instRefVals.setCusip(data.get("cusip"));
        instRefVals.setIsin(data.get("isin"));
        instRefVals.setRic(data.get("ric"));
        instRefVals.setSedol(data.get("sedol"));
        instRefVals.setTicker(data.get("ticker"));
        return instRefVals;
    }

    public static SpecificRecord populateData(prices_keys pricesKeys,
            Map<String, String> data) {
        pricesKeys.setTicker(data.get("ticker"));
        return pricesKeys;
    }

    public static SpecificRecord populateData(prices_values pricesVals,
            Map<String, String> data) {
        pricesVals.setCurr(data.get("curr"));
        pricesVals.setPrice(Double.parseDouble(data.get("price")));
        return pricesVals;
    }

    public static SpecificRecord populateData(
            position_data_keys positionKeys, Map<String, String> data) {
        positionKeys.setRic(data.get("ric"));
        positionKeys.setAccount(data.get("account"));
        positionKeys.setEffectiveDate(data.get("effective_date"));
        positionKeys.setKnowledgeDate(data.get("knowledge_date"));
        positionKeys.setPurpose(data.get("purpose"));
        positionKeys.setPositionType(data.get("position_type"));
        return positionKeys;
    }

    public static SpecificRecord populateData(
            position_data_values positionVals, Map<String, String> data) {
        positionVals.setDirection(data.get("direction"));
        positionVals.setQty(Integer.parseInt(data.get("qty")));
        return positionVals;
    }

    public static SpecificRecord[] populateData(Topic topic,
            SpecificRecord[] SpecificRecord, Map<String, String> data) {
        SpecificRecord updatedKey = SpecificRecord[0];
        SpecificRecord updatedVal = SpecificRecord[1];
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
        return new SpecificRecord[] {updatedKey, updatedVal};
    }


}
