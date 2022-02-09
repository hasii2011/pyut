package ozzee;


public class BaseModel implements ICreated, IModified {

    public  static  final   String  SYSTEM_USER = "System";
    private Long             id;

    private String  createdAttributes;
    private String  modifiedAttributes;

    public BaseModel() {

        createdAttributes  = "";
        modifiedAttributes = "";
    }
    public Long getId() {
        return id;
    }
    public void setId(Long id) {
        this.id = id;
    }
    @Override
    public String getCreatedAttributes() {
        return createdAttributes;
    }
    @Override
    public void setCreatedAttributes(String theCreatedAttributes) {
        createdAttributes = theCreatedAttributes;
    }
    @Override
    public String getModifiedAttributes() {
        return modifiedAttributes;
    }
    @Override
    public void setModifiedAttributes(String theModifiedAttributes) {
        modifiedAttributes = theModifiedAttributes;
    }

}
