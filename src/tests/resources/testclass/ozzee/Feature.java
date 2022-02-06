package ozzee;

import ozzee.Tenancy;

public class Feature implements Tenancy {

    private Tenant tenant;
    private String name;

    public Feature() {
    }

    public Tenant getTenant() {
        return tenant;
    }
    public void setTenant(Tenant tenant) {
        this.tenant = tenant;
    }

}