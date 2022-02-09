package ozzee;

public class Feature extends BaseModel implements Tenancy {

    private Tenant tenant;
    private String name;

    public Feature() {
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }

    @Override
    public Tenant getTenant() {
        return tenant;
    }
    @Override
    public void setTenant(Tenant tenant) {
        this.tenant = tenant;
    }

}