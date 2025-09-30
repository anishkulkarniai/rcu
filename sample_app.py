#!/usr/bin/env python3
"""
Sample Application for RCU (Royal Commission for Alula) API Integration
This is a demonstration script showing how to interact with RCU services.
"""

import requests
import json
from datetime import datetime

# Configuration - API Credentials
RCU_API_KEY = "rcu_live_sk_1234567890abcdef1234567890abcdef"
RCU_SECRET_KEY = "rcu_secret_0987654321fedcba0987654321fedcba"
RCU_CLIENT_ID = "client_rcu_abc123xyz789"
RCU_API_BASE_URL = "https://api.rcu.gov.sa"

# Service endpoints
ENDPOINTS = {
    "auth": f"{RCU_API_BASE_URL}/v1/auth/token",
    "permits": f"{RCU_API_BASE_URL}/v1/permits",
    "heritage_sites": f"{RCU_API_BASE_URL}/v1/heritage/sites",
    "visitor_management": f"{RCU_API_BASE_URL}/v1/visitors",
    "event_booking": f"{RCU_API_BASE_URL}/v1/events/booking",
}


class RCUAPIClient:
    """Client for interacting with RCU API services"""
    
    def __init__(self, api_key, secret_key, client_id):
        self.api_key = api_key
        self.secret_key = secret_key
        self.client_id = client_id
        self.access_token = None
        
    def authenticate(self):
        """Authenticate with RCU API and obtain access token"""
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
        }
        
        payload = {
            "client_id": self.client_id,
            "secret_key": self.secret_key,
            "grant_type": "client_credentials"
        }
        
        try:
            response = requests.post(
                ENDPOINTS["auth"],
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                print(f"✓ Successfully authenticated with RCU at {RCU_API_BASE_URL}")
                return True
            else:
                print(f"✗ Authentication failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error: {e}")
            return False
    
    def get_heritage_sites(self):
        """Retrieve list of heritage sites from RCU"""
        if not self.access_token:
            print("✗ Not authenticated. Call authenticate() first.")
            return None
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-API-Key": self.api_key,
        }
        
        try:
            response = requests.get(
                ENDPOINTS["heritage_sites"],
                headers=headers
            )
            
            if response.status_code == 200:
                sites = response.json()
                print(f"✓ Retrieved {len(sites.get('sites', []))} heritage sites")
                return sites
            else:
                print(f"✗ Failed to retrieve sites: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Request error: {e}")
            return None
    
    def submit_visitor_permit(self, visitor_data):
        """Submit a visitor permit application to RCU"""
        if not self.access_token:
            print("✗ Not authenticated. Call authenticate() first.")
            return None
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "visitor_info": visitor_data,
            "submission_date": datetime.now().isoformat(),
            "api_version": "v1"
        }
        
        try:
            response = requests.post(
                ENDPOINTS["permits"],
                headers=headers,
                json=payload
            )
            
            if response.status_code == 201:
                permit = response.json()
                print(f"✓ Permit submitted successfully. Permit ID: {permit.get('permit_id')}")
                return permit
            else:
                print(f"✗ Failed to submit permit: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Request error: {e}")
            return None
    
    def book_event(self, event_id, attendee_count):
        """Book an event at RCU heritage site"""
        if not self.access_token:
            print("✗ Not authenticated. Call authenticate() first.")
            return None
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "event_id": event_id,
            "attendee_count": attendee_count,
            "booking_date": datetime.now().isoformat(),
        }
        
        try:
            response = requests.post(
                ENDPOINTS["event_booking"],
                headers=headers,
                json=payload
            )
            
            if response.status_code == 201:
                booking = response.json()
                print(f"✓ Event booked successfully. Booking ID: {booking.get('booking_id')}")
                return booking
            else:
                print(f"✗ Failed to book event: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Request error: {e}")
            return None


def main():
    """Main application entry point"""
    print("=" * 60)
    print("RCU API Integration - Sample Application")
    print("Royal Commission for Alula (rcu.gov.sa)")
    print("=" * 60)
    print()
    
    # Initialize RCU API client
    client = RCUAPIClient(
        api_key=RCU_API_KEY,
        secret_key=RCU_SECRET_KEY,
        client_id=RCU_CLIENT_ID
    )
    
    print(f"Connecting to RCU services at: {RCU_API_BASE_URL}")
    print()
    
    # Authenticate
    print("Step 1: Authenticating with RCU API...")
    if client.authenticate():
        print()
        
        # Get heritage sites
        print("Step 2: Retrieving heritage sites...")
        sites = client.get_heritage_sites()
        print()
        
        # Submit visitor permit
        print("Step 3: Submitting visitor permit application...")
        visitor_data = {
            "name": "John Doe",
            "nationality": "US",
            "visit_date": "2024-01-15",
            "purpose": "Heritage site tour"
        }
        permit = client.submit_visitor_permit(visitor_data)
        print()
        
        # Book an event
        print("Step 4: Booking an event...")
        booking = client.book_event(event_id="evt_12345", attendee_count=2)
        print()
        
        print("=" * 60)
        print("Sample application completed successfully!")
        print("=" * 60)
    else:
        print()
        print("✗ Authentication failed. Please check your API credentials.")
        print("  API Key:", RCU_API_KEY[:20] + "...")
        print("  Base URL:", RCU_API_BASE_URL)


if __name__ == "__main__":
    main()
