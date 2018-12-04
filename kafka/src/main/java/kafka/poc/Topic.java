package kafka.poc;

public enum Topic {
    INST_REF ("inst-ref"),
    PRICES ("prices"),
    POSITION ("position");

    private final String name;

    private Topic (String s){
        name = s;
    }

    public boolean equalsName(String otherName){
        return name.equals(otherName);
    }

    @Override
    public String toString(){
        return this.name;
    }
}