ola_queries.sql
-- 1. Retrieve all successful bookings:
SELECT * FROM rides WHERE Booking_Status = 'Successful';


-- 2. Find the average ride distance for each vehicle type:
SELECT
    Vehicle_Type,
    AVG(Ride_Distance) AS average_distance
FROM rides
WHERE Booking_Status = 'Success'
GROUP BY Vehicle_Type;


-- 3. Get the total number of cancelled rides by customers:
SELECT
    COUNT(Booking_ID) AS total_customer_cancellations
FROM rides
WHERE Booking_Status = 'Canceled by Customer';


-- 4. List the top 5 customers who booked the highest number of rides:
SELECT
    Customer_ID,
    COUNT(Booking_ID) AS ride_count
FROM rides
GROUP BY Customer_ID
ORDER BY ride_count DESC
LIMIT 5;


-- 5. Get the number of rides cancelled by drivers due to personal/car issues:
SELECT
    Canceled_Rides_by_Driver,
    COUNT(Booking_ID) AS cancellation_count
FROM rides
WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue'
GROUP BY Canceled_Rides_by_Driver;


-- 6. Find the maximum and minimum driver ratings for Prime Sedan bookings:
SELECT
    MAX(Driver_Ratings) AS max_rating,
    MIN(Driver_Ratings) AS min_rating
FROM rides
WHERE Vehicle_Type = 'Prime Sedan' AND Driver_Ratings IS NOT NULL;


-- 7. Retrieve all rides where payment was made using UPI:
SELECT * FROM rides WHERE Payment_Method = 'UPI';


-- 8. Find the average driver rating per vehicle type:
SELECT
    Vehicle_Type,
    AVG(Driver_Ratings) AS avg_driver_rating
FROM rides
WHERE Booking_Status = 'Success' AND Driver_Ratings IS NOT NULL
GROUP BY Vehicle_Type;


-- 9. Calculate the total booking value of rides completed successfully:
SELECT
    SUM(Booking_Value) AS total_revenue
FROM rides
WHERE Booking_Status = 'Success';


-- 10. List all incomplete rides along with the reason:
SELECT
    Booking_ID,
    Booking_Status,
    Cancellation_Reason
FROM rides
WHERE Booking_Status != 'Success';
