<?php
require_once 'vendor/autoload.php'; // Include Composer autoload file

use Kreait\Firebase\Factory;
use Kreait\Firebase\ServiceAccount;

class FirebaseService {
    private $database;

    public function __construct() {
        // Initialize Firebase with your service account credentials
        $serviceAccount = ServiceAccount::fromJsonFile(__DIR__ . '/barber-c4424-firebase-adminsdk-meiwp-e73b31a900.json');
        $firebase = (new Factory)
            ->withServiceAccount($serviceAccount)
            ->createFirestore();

        $this->database = $firebase->database();
    }

    public function fetchBookings() {
        // Get today's and tomorrow's date in YYYY-MM-DD format
        $today = date('Y-m-d');
        $tomorrow = date('Y-m-d', strtotime('+1 day'));

        // Fetch bookings from Firestore collection
        $bookingsRef = $this->database->collection('bookings');
        $bookings = $bookingsRef->where('date', 'in', [$today, $tomorrow])->documents();

        $bookingList = [];
        foreach ($bookings as $booking) {
            $bookingList[] = $booking->data();
        }

        return $bookingList;
    }
}
