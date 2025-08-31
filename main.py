from Data_Through_APIS import Linkedin


def get_linkedin_jobs():
    Role = input("Enter the Role you want to search for: ")
    Location = input("Enter the Location you want to search in: ")
    Linkedin.get_linkedin_jobs(Role, Location)


