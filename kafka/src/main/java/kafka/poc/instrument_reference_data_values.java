/**
 * Autogenerated by Avro
 *
 * DO NOT EDIT DIRECTLY
 */
package kafka.poc;

import org.apache.avro.specific.SpecificData;
import org.apache.avro.message.BinaryMessageEncoder;
import org.apache.avro.message.BinaryMessageDecoder;
import org.apache.avro.message.SchemaStore;

@SuppressWarnings("all")
@org.apache.avro.specific.AvroGenerated
public class instrument_reference_data_values extends org.apache.avro.specific.SpecificRecordBase implements org.apache.avro.specific.SpecificRecord {
  private static final long serialVersionUID = -4126788069297184264L;
  public static final org.apache.avro.Schema SCHEMA$ = new org.apache.avro.Schema.Parser().parse("{\"type\":\"record\",\"name\":\"instrument_reference_data_values\",\"namespace\":\"kafka.poc\",\"fields\":[{\"name\":\"asset_class\",\"type\":\"string\"},{\"name\":\"coi\",\"type\":\"string\"},{\"name\":\"ric\",\"type\":\"string\"},{\"name\":\"isin\",\"type\":\"string\"},{\"name\":\"sedol\",\"type\":\"string\"},{\"name\":\"ticker\",\"type\":\"string\"},{\"name\":\"cusip\",\"type\":\"string\"}]}");
  public static org.apache.avro.Schema getClassSchema() { return SCHEMA$; }

  private static SpecificData MODEL$ = new SpecificData();

  private static final BinaryMessageEncoder<instrument_reference_data_values> ENCODER =
      new BinaryMessageEncoder<instrument_reference_data_values>(MODEL$, SCHEMA$);

  private static final BinaryMessageDecoder<instrument_reference_data_values> DECODER =
      new BinaryMessageDecoder<instrument_reference_data_values>(MODEL$, SCHEMA$);

  /**
   * Return the BinaryMessageDecoder instance used by this class.
   */
  public static BinaryMessageDecoder<instrument_reference_data_values> getDecoder() {
    return DECODER;
  }

  /**
   * Create a new BinaryMessageDecoder instance for this class that uses the specified {@link SchemaStore}.
   * @param resolver a {@link SchemaStore} used to find schemas by fingerprint
   */
  public static BinaryMessageDecoder<instrument_reference_data_values> createDecoder(SchemaStore resolver) {
    return new BinaryMessageDecoder<instrument_reference_data_values>(MODEL$, SCHEMA$, resolver);
  }

  /** Serializes this instrument_reference_data_values to a ByteBuffer. */
  public java.nio.ByteBuffer toByteBuffer() throws java.io.IOException {
    return ENCODER.encode(this);
  }

  /** Deserializes a instrument_reference_data_values from a ByteBuffer. */
  public static instrument_reference_data_values fromByteBuffer(
      java.nio.ByteBuffer b) throws java.io.IOException {
    return DECODER.decode(b);
  }

  @Deprecated public java.lang.CharSequence asset_class;
  @Deprecated public java.lang.CharSequence coi;
  @Deprecated public java.lang.CharSequence ric;
  @Deprecated public java.lang.CharSequence isin;
  @Deprecated public java.lang.CharSequence sedol;
  @Deprecated public java.lang.CharSequence ticker;
  @Deprecated public java.lang.CharSequence cusip;

  /**
   * Default constructor.  Note that this does not initialize fields
   * to their default values from the schema.  If that is desired then
   * one should use <code>newBuilder()</code>.
   */
  public instrument_reference_data_values() {}

  /**
   * All-args constructor.
   * @param asset_class The new value for asset_class
   * @param coi The new value for coi
   * @param ric The new value for ric
   * @param isin The new value for isin
   * @param sedol The new value for sedol
   * @param ticker The new value for ticker
   * @param cusip The new value for cusip
   */
  public instrument_reference_data_values(java.lang.CharSequence asset_class, java.lang.CharSequence coi, java.lang.CharSequence ric, java.lang.CharSequence isin, java.lang.CharSequence sedol, java.lang.CharSequence ticker, java.lang.CharSequence cusip) {
    this.asset_class = asset_class;
    this.coi = coi;
    this.ric = ric;
    this.isin = isin;
    this.sedol = sedol;
    this.ticker = ticker;
    this.cusip = cusip;
  }

  public org.apache.avro.Schema getSchema() { return SCHEMA$; }
  // Used by DatumWriter.  Applications should not call.
  public java.lang.Object get(int field$) {
    switch (field$) {
    case 0: return asset_class;
    case 1: return coi;
    case 2: return ric;
    case 3: return isin;
    case 4: return sedol;
    case 5: return ticker;
    case 6: return cusip;
    default: throw new org.apache.avro.AvroRuntimeException("Bad index");
    }
  }

  // Used by DatumReader.  Applications should not call.
  @SuppressWarnings(value="unchecked")
  public void put(int field$, java.lang.Object value$) {
    switch (field$) {
    case 0: asset_class = (java.lang.CharSequence)value$; break;
    case 1: coi = (java.lang.CharSequence)value$; break;
    case 2: ric = (java.lang.CharSequence)value$; break;
    case 3: isin = (java.lang.CharSequence)value$; break;
    case 4: sedol = (java.lang.CharSequence)value$; break;
    case 5: ticker = (java.lang.CharSequence)value$; break;
    case 6: cusip = (java.lang.CharSequence)value$; break;
    default: throw new org.apache.avro.AvroRuntimeException("Bad index");
    }
  }

  /**
   * Gets the value of the 'asset_class' field.
   * @return The value of the 'asset_class' field.
   */
  public java.lang.CharSequence getAssetClass() {
    return asset_class;
  }

  /**
   * Sets the value of the 'asset_class' field.
   * @param value the value to set.
   */
  public void setAssetClass(java.lang.CharSequence value) {
    this.asset_class = value;
  }

  /**
   * Gets the value of the 'coi' field.
   * @return The value of the 'coi' field.
   */
  public java.lang.CharSequence getCoi() {
    return coi;
  }

  /**
   * Sets the value of the 'coi' field.
   * @param value the value to set.
   */
  public void setCoi(java.lang.CharSequence value) {
    this.coi = value;
  }

  /**
   * Gets the value of the 'ric' field.
   * @return The value of the 'ric' field.
   */
  public java.lang.CharSequence getRic() {
    return ric;
  }

  /**
   * Sets the value of the 'ric' field.
   * @param value the value to set.
   */
  public void setRic(java.lang.CharSequence value) {
    this.ric = value;
  }

  /**
   * Gets the value of the 'isin' field.
   * @return The value of the 'isin' field.
   */
  public java.lang.CharSequence getIsin() {
    return isin;
  }

  /**
   * Sets the value of the 'isin' field.
   * @param value the value to set.
   */
  public void setIsin(java.lang.CharSequence value) {
    this.isin = value;
  }

  /**
   * Gets the value of the 'sedol' field.
   * @return The value of the 'sedol' field.
   */
  public java.lang.CharSequence getSedol() {
    return sedol;
  }

  /**
   * Sets the value of the 'sedol' field.
   * @param value the value to set.
   */
  public void setSedol(java.lang.CharSequence value) {
    this.sedol = value;
  }

  /**
   * Gets the value of the 'ticker' field.
   * @return The value of the 'ticker' field.
   */
  public java.lang.CharSequence getTicker() {
    return ticker;
  }

  /**
   * Sets the value of the 'ticker' field.
   * @param value the value to set.
   */
  public void setTicker(java.lang.CharSequence value) {
    this.ticker = value;
  }

  /**
   * Gets the value of the 'cusip' field.
   * @return The value of the 'cusip' field.
   */
  public java.lang.CharSequence getCusip() {
    return cusip;
  }

  /**
   * Sets the value of the 'cusip' field.
   * @param value the value to set.
   */
  public void setCusip(java.lang.CharSequence value) {
    this.cusip = value;
  }

  /**
   * Creates a new instrument_reference_data_values RecordBuilder.
   * @return A new instrument_reference_data_values RecordBuilder
   */
  public static kafka.poc.instrument_reference_data_values.Builder newBuilder() {
    return new kafka.poc.instrument_reference_data_values.Builder();
  }

  /**
   * Creates a new instrument_reference_data_values RecordBuilder by copying an existing Builder.
   * @param other The existing builder to copy.
   * @return A new instrument_reference_data_values RecordBuilder
   */
  public static kafka.poc.instrument_reference_data_values.Builder newBuilder(kafka.poc.instrument_reference_data_values.Builder other) {
    return new kafka.poc.instrument_reference_data_values.Builder(other);
  }

  /**
   * Creates a new instrument_reference_data_values RecordBuilder by copying an existing instrument_reference_data_values instance.
   * @param other The existing instance to copy.
   * @return A new instrument_reference_data_values RecordBuilder
   */
  public static kafka.poc.instrument_reference_data_values.Builder newBuilder(kafka.poc.instrument_reference_data_values other) {
    return new kafka.poc.instrument_reference_data_values.Builder(other);
  }

  /**
   * RecordBuilder for instrument_reference_data_values instances.
   */
  public static class Builder extends org.apache.avro.specific.SpecificRecordBuilderBase<instrument_reference_data_values>
    implements org.apache.avro.data.RecordBuilder<instrument_reference_data_values> {

    private java.lang.CharSequence asset_class;
    private java.lang.CharSequence coi;
    private java.lang.CharSequence ric;
    private java.lang.CharSequence isin;
    private java.lang.CharSequence sedol;
    private java.lang.CharSequence ticker;
    private java.lang.CharSequence cusip;

    /** Creates a new Builder */
    private Builder() {
      super(SCHEMA$);
    }

    /**
     * Creates a Builder by copying an existing Builder.
     * @param other The existing Builder to copy.
     */
    private Builder(kafka.poc.instrument_reference_data_values.Builder other) {
      super(other);
      if (isValidValue(fields()[0], other.asset_class)) {
        this.asset_class = data().deepCopy(fields()[0].schema(), other.asset_class);
        fieldSetFlags()[0] = true;
      }
      if (isValidValue(fields()[1], other.coi)) {
        this.coi = data().deepCopy(fields()[1].schema(), other.coi);
        fieldSetFlags()[1] = true;
      }
      if (isValidValue(fields()[2], other.ric)) {
        this.ric = data().deepCopy(fields()[2].schema(), other.ric);
        fieldSetFlags()[2] = true;
      }
      if (isValidValue(fields()[3], other.isin)) {
        this.isin = data().deepCopy(fields()[3].schema(), other.isin);
        fieldSetFlags()[3] = true;
      }
      if (isValidValue(fields()[4], other.sedol)) {
        this.sedol = data().deepCopy(fields()[4].schema(), other.sedol);
        fieldSetFlags()[4] = true;
      }
      if (isValidValue(fields()[5], other.ticker)) {
        this.ticker = data().deepCopy(fields()[5].schema(), other.ticker);
        fieldSetFlags()[5] = true;
      }
      if (isValidValue(fields()[6], other.cusip)) {
        this.cusip = data().deepCopy(fields()[6].schema(), other.cusip);
        fieldSetFlags()[6] = true;
      }
    }

    /**
     * Creates a Builder by copying an existing instrument_reference_data_values instance
     * @param other The existing instance to copy.
     */
    private Builder(kafka.poc.instrument_reference_data_values other) {
            super(SCHEMA$);
      if (isValidValue(fields()[0], other.asset_class)) {
        this.asset_class = data().deepCopy(fields()[0].schema(), other.asset_class);
        fieldSetFlags()[0] = true;
      }
      if (isValidValue(fields()[1], other.coi)) {
        this.coi = data().deepCopy(fields()[1].schema(), other.coi);
        fieldSetFlags()[1] = true;
      }
      if (isValidValue(fields()[2], other.ric)) {
        this.ric = data().deepCopy(fields()[2].schema(), other.ric);
        fieldSetFlags()[2] = true;
      }
      if (isValidValue(fields()[3], other.isin)) {
        this.isin = data().deepCopy(fields()[3].schema(), other.isin);
        fieldSetFlags()[3] = true;
      }
      if (isValidValue(fields()[4], other.sedol)) {
        this.sedol = data().deepCopy(fields()[4].schema(), other.sedol);
        fieldSetFlags()[4] = true;
      }
      if (isValidValue(fields()[5], other.ticker)) {
        this.ticker = data().deepCopy(fields()[5].schema(), other.ticker);
        fieldSetFlags()[5] = true;
      }
      if (isValidValue(fields()[6], other.cusip)) {
        this.cusip = data().deepCopy(fields()[6].schema(), other.cusip);
        fieldSetFlags()[6] = true;
      }
    }

    /**
      * Gets the value of the 'asset_class' field.
      * @return The value.
      */
    public java.lang.CharSequence getAssetClass() {
      return asset_class;
    }

    /**
      * Sets the value of the 'asset_class' field.
      * @param value The value of 'asset_class'.
      * @return This builder.
      */
    public kafka.poc.instrument_reference_data_values.Builder setAssetClass(java.lang.CharSequence value) {
      validate(fields()[0], value);
      this.asset_class = value;
      fieldSetFlags()[0] = true;
      return this;
    }

    /**
      * Checks whether the 'asset_class' field has been set.
      * @return True if the 'asset_class' field has been set, false otherwise.
      */
    public boolean hasAssetClass() {
      return fieldSetFlags()[0];
    }


    /**
      * Clears the value of the 'asset_class' field.
      * @return This builder.
      */
    public kafka.poc.instrument_reference_data_values.Builder clearAssetClass() {
      asset_class = null;
      fieldSetFlags()[0] = false;
      return this;
    }

    /**
      * Gets the value of the 'coi' field.
      * @return The value.
      */
    public java.lang.CharSequence getCoi() {
      return coi;
    }

    /**
      * Sets the value of the 'coi' field.
      * @param value The value of 'coi'.
      * @return This builder.
      */
    public kafka.poc.instrument_reference_data_values.Builder setCoi(java.lang.CharSequence value) {
      validate(fields()[1], value);
      this.coi = value;
      fieldSetFlags()[1] = true;
      return this;
    }

    /**
      * Checks whether the 'coi' field has been set.
      * @return True if the 'coi' field has been set, false otherwise.
      */
    public boolean hasCoi() {
      return fieldSetFlags()[1];
    }


    /**
      * Clears the value of the 'coi' field.
      * @return This builder.
      */
    public kafka.poc.instrument_reference_data_values.Builder clearCoi() {
      coi = null;
      fieldSetFlags()[1] = false;
      return this;
    }

    /**
      * Gets the value of the 'ric' field.
      * @return The value.
      */
    public java.lang.CharSequence getRic() {
      return ric;
    }

    /**
      * Sets the value of the 'ric' field.
      * @param value The value of 'ric'.
      * @return This builder.
      */
    public kafka.poc.instrument_reference_data_values.Builder setRic(java.lang.CharSequence value) {
      validate(fields()[2], value);
      this.ric = value;
      fieldSetFlags()[2] = true;
      return this;
    }

    /**
      * Checks whether the 'ric' field has been set.
      * @return True if the 'ric' field has been set, false otherwise.
      */
    public boolean hasRic() {
      return fieldSetFlags()[2];
    }


    /**
      * Clears the value of the 'ric' field.
      * @return This builder.
      */
    public kafka.poc.instrument_reference_data_values.Builder clearRic() {
      ric = null;
      fieldSetFlags()[2] = false;
      return this;
    }

    /**
      * Gets the value of the 'isin' field.
      * @return The value.
      */
    public java.lang.CharSequence getIsin() {
      return isin;
    }

    /**
      * Sets the value of the 'isin' field.
      * @param value The value of 'isin'.
      * @return This builder.
      */
    public kafka.poc.instrument_reference_data_values.Builder setIsin(java.lang.CharSequence value) {
      validate(fields()[3], value);
      this.isin = value;
      fieldSetFlags()[3] = true;
      return this;
    }

    /**
      * Checks whether the 'isin' field has been set.
      * @return True if the 'isin' field has been set, false otherwise.
      */
    public boolean hasIsin() {
      return fieldSetFlags()[3];
    }


    /**
      * Clears the value of the 'isin' field.
      * @return This builder.
      */
    public kafka.poc.instrument_reference_data_values.Builder clearIsin() {
      isin = null;
      fieldSetFlags()[3] = false;
      return this;
    }

    /**
      * Gets the value of the 'sedol' field.
      * @return The value.
      */
    public java.lang.CharSequence getSedol() {
      return sedol;
    }

    /**
      * Sets the value of the 'sedol' field.
      * @param value The value of 'sedol'.
      * @return This builder.
      */
    public kafka.poc.instrument_reference_data_values.Builder setSedol(java.lang.CharSequence value) {
      validate(fields()[4], value);
      this.sedol = value;
      fieldSetFlags()[4] = true;
      return this;
    }

    /**
      * Checks whether the 'sedol' field has been set.
      * @return True if the 'sedol' field has been set, false otherwise.
      */
    public boolean hasSedol() {
      return fieldSetFlags()[4];
    }


    /**
      * Clears the value of the 'sedol' field.
      * @return This builder.
      */
    public kafka.poc.instrument_reference_data_values.Builder clearSedol() {
      sedol = null;
      fieldSetFlags()[4] = false;
      return this;
    }

    /**
      * Gets the value of the 'ticker' field.
      * @return The value.
      */
    public java.lang.CharSequence getTicker() {
      return ticker;
    }

    /**
      * Sets the value of the 'ticker' field.
      * @param value The value of 'ticker'.
      * @return This builder.
      */
    public kafka.poc.instrument_reference_data_values.Builder setTicker(java.lang.CharSequence value) {
      validate(fields()[5], value);
      this.ticker = value;
      fieldSetFlags()[5] = true;
      return this;
    }

    /**
      * Checks whether the 'ticker' field has been set.
      * @return True if the 'ticker' field has been set, false otherwise.
      */
    public boolean hasTicker() {
      return fieldSetFlags()[5];
    }


    /**
      * Clears the value of the 'ticker' field.
      * @return This builder.
      */
    public kafka.poc.instrument_reference_data_values.Builder clearTicker() {
      ticker = null;
      fieldSetFlags()[5] = false;
      return this;
    }

    /**
      * Gets the value of the 'cusip' field.
      * @return The value.
      */
    public java.lang.CharSequence getCusip() {
      return cusip;
    }

    /**
      * Sets the value of the 'cusip' field.
      * @param value The value of 'cusip'.
      * @return This builder.
      */
    public kafka.poc.instrument_reference_data_values.Builder setCusip(java.lang.CharSequence value) {
      validate(fields()[6], value);
      this.cusip = value;
      fieldSetFlags()[6] = true;
      return this;
    }

    /**
      * Checks whether the 'cusip' field has been set.
      * @return True if the 'cusip' field has been set, false otherwise.
      */
    public boolean hasCusip() {
      return fieldSetFlags()[6];
    }


    /**
      * Clears the value of the 'cusip' field.
      * @return This builder.
      */
    public kafka.poc.instrument_reference_data_values.Builder clearCusip() {
      cusip = null;
      fieldSetFlags()[6] = false;
      return this;
    }

    @Override
    @SuppressWarnings("unchecked")
    public instrument_reference_data_values build() {
      try {
        instrument_reference_data_values record = new instrument_reference_data_values();
        record.asset_class = fieldSetFlags()[0] ? this.asset_class : (java.lang.CharSequence) defaultValue(fields()[0]);
        record.coi = fieldSetFlags()[1] ? this.coi : (java.lang.CharSequence) defaultValue(fields()[1]);
        record.ric = fieldSetFlags()[2] ? this.ric : (java.lang.CharSequence) defaultValue(fields()[2]);
        record.isin = fieldSetFlags()[3] ? this.isin : (java.lang.CharSequence) defaultValue(fields()[3]);
        record.sedol = fieldSetFlags()[4] ? this.sedol : (java.lang.CharSequence) defaultValue(fields()[4]);
        record.ticker = fieldSetFlags()[5] ? this.ticker : (java.lang.CharSequence) defaultValue(fields()[5]);
        record.cusip = fieldSetFlags()[6] ? this.cusip : (java.lang.CharSequence) defaultValue(fields()[6]);
        return record;
      } catch (java.lang.Exception e) {
        throw new org.apache.avro.AvroRuntimeException(e);
      }
    }
  }

  @SuppressWarnings("unchecked")
  private static final org.apache.avro.io.DatumWriter<instrument_reference_data_values>
    WRITER$ = (org.apache.avro.io.DatumWriter<instrument_reference_data_values>)MODEL$.createDatumWriter(SCHEMA$);

  @Override public void writeExternal(java.io.ObjectOutput out)
    throws java.io.IOException {
    WRITER$.write(this, SpecificData.getEncoder(out));
  }

  @SuppressWarnings("unchecked")
  private static final org.apache.avro.io.DatumReader<instrument_reference_data_values>
    READER$ = (org.apache.avro.io.DatumReader<instrument_reference_data_values>)MODEL$.createDatumReader(SCHEMA$);

  @Override public void readExternal(java.io.ObjectInput in)
    throws java.io.IOException {
    READER$.read(this, SpecificData.getDecoder(in));
  }

}
