/*
 * This program, Coordinates.java, asks for the user's
 * area of interest(AOI), then once the user enters their
 * AOI, the program accesses an SQL database and retrieves
 * the area of interest, longitude, and latitude value.
 *
 * Creator: Saravana Polisetti
 * Finished: 7/17/2020
 */

import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Coordinates {

    public static void main(String[] args) {
        System.out.print("What is you area of interest(AOI) number: ");
        Scanner input = new Scanner(System.in); // creates an instance of the scanner class to retrieve the user's AOI
        int response = input.nextInt();// the int variable int is assigned the user's AOI number

        AOI(response);// calls the AOI method to retrieve the AOI, Longitude, and the Latitude
    }
    public static void AOI(double AOI_Num)
    {
        List<Coordinates2> result = new ArrayList<>();// result will be a bunch of rows from the results from the query's from the sql
        String longAndLat = "SELECT * FROM \"Coordinates\" WHERE \"AOI_Number\" = " + AOI_Num;// gives the string variable the query to retrieve the area of interest, longitude, and latitude from the database

        try
        {
            Connection connection = DriverManager.getConnection("jdbc:postgresql://127.0.0.1:5432/java_class", "postgres", "postgres123");// connects SQL to the program, bridges them
            PreparedStatement preparedStatement = connection.prepareStatement(longAndLat);// string from line 18 is made into an actual query statement here
            {

                /*
                 * A ResultSet object(resultSet) is a table of data
                 * representing a database result set.The statement
                 * below takes the longAndLat(now an SQL query) from
                 * line 18 and then it executes it and the result is
                 *  then put into resultSet.
                 */
                ResultSet resultSet = preparedStatement.executeQuery();

                while (resultSet.next()) // goes through each row in resultSet
                {
                    /*
                     * Remember that resultSet is a table of data, so here
                     * we are retrieving values from the columns -- AOI_Number,
                     * Longitude, and Latitude -- and assigning them to AOI_Number,
                     * Longitude, Latitude respectively.
                     */
                    int AOI_Number = resultSet.getInt("AOI_Number");
                    double Longitude = resultSet.getDouble("Longitude");
                    double Latitude = resultSet.getDouble("Latitude");

                    Coordinates2 store = new Coordinates2(); // creates an object(store) to store the values: AOI, Longitude, Latitude
                    store.setAOI_Number(AOI_Number);
                    store.setLatitude(Latitude);
                    store.setLongitude(Longitude);
                    System.out.println("These are your coordinates(Longitude, Latitude) for AOI number "
                            + store.getAOI_Number() + ": " + "(" + store.getLongitude() + ", " + store.getLatitude() + ")");
                    System.out.println();
                    result.add(store);// adds the object, store, into the List, result(instantiated and declared on line 27)

                }
            }
        }

        catch (Exception e)
        {
            e.printStackTrace();
        }
    }
}