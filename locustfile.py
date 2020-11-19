The focus of this lesson isn’t to teach you how to use locust but we will go over the below code:

from locust import HttpUser, task, between
from faker import Faker
import uuid
import random
import time

class QuickstartUser(HttpUser):
    wait_time = between(1,4)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.books = []
        self.faker = Faker()
        self.token = None
    
    def on_start(self):
        id = str(uuid.uuid4())
        while self.token == None:
            try:
                self.client.post(
                    "/auth/register", 
                    json={"email": f"test{id}@test.com", "password":"secret"}
                )
                response = self.client.post(
                    "/auth/login", 
                    json={"email": f"test{id}@test.com", "password":"secret"}
                )
                self.token = response.json()["token"]
            except:
                time.sleep(3)
    
    @task
    def index_page(self):
        self.client.get("/books/")
    
    @task(3)
    def create_book(self):
        if self.token:
            response = self.client.post(
                "/books/",
                json={ "title": self.faker.catch_phrase() },
                headers={ "Authorization": f"Bearer {self.token}"}
            )
            if response.status_code < 400:
                self.books.append(response.json()["id"])
    
    @task(2)
    def update_book(self):
        if len(self.books) > 0 and self.token:
            book_id = random.choice(self.books)
            self.client.put(
                f"/books/{book_id}", 
                json={ "title": self.faker.catch_phrase() },
                headers={ "Authorization": f"Bearer {self.token}"}
            )
    
    @task(2)
    def delete_book(self):
        if len(self.books) > 0 and self.token:
            book_id = random.choice(self.books)
            response = self.client.delete(
                f"/books/{book_id}",
                headers={ "Authorization": f"Bearer {self.token}"}
            )
            if response.status_code < 400:
                self.books.remove(book_id)