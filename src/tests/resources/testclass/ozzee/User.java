package ozzee;

public class User extends BaseModel {


    private String          name;
    private String          tcsId;

    public User() {
    }
    public User(String theName, String theTcsId) {

        name = theName;
        tcsId = theTcsId;
    }

}
