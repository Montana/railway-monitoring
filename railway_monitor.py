#!/usr/bin/env python3

import requests
import sys
import time
from datetime import datetime
import json
import os

class RailwayChecker:
    def __init__(self, api_token=None, project_id=None, service_id=None):
        self.api_token = api_token or os.getenv('RAILWAY_TOKEN')
        self.project_id = project_id or os.getenv('RAILWAY_PROJECT_ID')
        self.service_id = service_id or os.getenv('RAILWAY_SERVICE_ID')
        self.base_url = "https://backboard.railway.app/graphql"
        
    def check_api_health(self):
        headers = {}
        if self.api_token:
            headers['Authorization'] = f'Bearer {self.api_token}'
            headers['Content-Type'] = 'application/json'
        
        query = """
        query {
            me {
                id
                email
            }
        }
        """
        
        try:
            response = requests.post(
                self.base_url,
                json={'query': query},
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'errors' in data:
                    return False, f"API Error: {data['errors']}"
                return True, "Railway API is accessible"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"
    
    def check_deployment_url(self, url):
        try:
            response = requests.get(url, timeout=10)
            return {
                'accessible': True,
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'ok': response.ok
            }
        except requests.exceptions.RequestException as e:
            return {
                'accessible': False,
                'error': str(e)
            }
    
    def get_project_info(self):
        if not self.api_token or not self.project_id:
            return None, "API token and project ID required"
        
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        query = """
        query project($id: String!) {
            project(id: $id) {
                id
                name
                description
                createdAt
                services {
                    edges {
                        node {
                            id
                            name
                            createdAt
                        }
                    }
                }
            }
        }
        """
        
        try:
            response = requests.post(
                self.base_url,
                json={
                    'query': query,
                    'variables': {'id': self.project_id}
                },
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'errors' in data:
                    return None, f"API Error: {data['errors']}"
                return data.get('data', {}).get('project'), None
            else:
                return None, f"HTTP {response.status_code}"
        except requests.exceptions.RequestException as e:
            return None, f"Connection error: {str(e)}"
    
    def run_full_check(self, deployment_url=None):
        print("=" * 60)
        print("Railway Instance Health Check")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("1. Checking Railway API connectivity...")
        api_ok, api_msg = self.check_api_health()
        print(f"   {api_msg}")
        print()
        
        if self.api_token and self.project_id:
            print("2. Checking project information...")
            project_info, error = self.get_project_info()
            if project_info:
                print(f"   Project: {project_info.get('name', 'N/A')}")
                print(f"   ID: {project_info.get('id', 'N/A')}")
                services = project_info.get('services', {}).get('edges', [])
                print(f"   Services: {len(services)}")
                for service in services:
                    node = service.get('node', {})
                    print(f"     - {node.get('name', 'Unknown')}")
            else:
                print(f"   {error}")
            print()
        
        if deployment_url:
            print("3. Checking deployment URL...")
            result = self.check_deployment_url(deployment_url)
            if result['accessible']:
                print(f"   URL: {deployment_url}")
                print(f"   Status: {result['status_code']}")
                print(f"   Response Time: {result['response_time']:.2f}s")
                print(f"   OK: {result['ok']}")
            else:
                print(f"   Failed: {result['error']}")
            print()
        
        print("=" * 60)
        return api_ok

def main():
    if len(sys.argv) > 1:
        deployment_url = sys.argv[1]
    else:
        deployment_url = os.getenv('RAILWAY_DEPLOYMENT_URL')
    
    checker = RailwayChecker()
    
    if not checker.api_token:
        print("Warning: RAILWAY_TOKEN not set. API checks will be limited.")
    if not checker.project_id:
        print("Warning: RAILWAY_PROJECT_ID not set. Project info unavailable.")
    
    print()
    success = checker.run_full_check(deployment_url)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
