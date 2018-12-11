package kafka.poc;

public enum Counter {
    SENT ("Sent Counter"),
    RECEIVED ("Received Counter"),
    ERROR ("Error Counter");

    private final String name;

    private Counter (String s){
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