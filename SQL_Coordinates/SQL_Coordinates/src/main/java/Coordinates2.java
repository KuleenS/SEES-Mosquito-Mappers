class Coordinates2 {

    private int AOI_Number;
    private double Latitude;
    private double Longitude;

    public Coordinates2()
    {
        AOI_Number = 0;
        Latitude = 0.0;
        Longitude = 0.0;
    }

    public int getAOI_Number() {
        return AOI_Number;
    }

    public double getLatitude() {
        return Latitude;
    }

    public double getLongitude() {
        return Longitude;
    }

    public void setAOI_Number(int AOI_Number) {
        this.AOI_Number = AOI_Number;
    }

    public void setLatitude(double Latitude) {
        this.Latitude = Latitude;
    }

    public void setLongitude(double Longitude) {
        this.Longitude = Longitude;
    }
}