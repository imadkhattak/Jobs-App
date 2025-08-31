
from Final_Code.glassdoor import glassdoor_data
from Final_Code.indeed import indeed_data
from Final_Code.Linkedin import get_linkedin_jobs

def main():
    print("Choose a platform to get job data from:")
    print("1. Glassdoor")
    print("2. Indeed")
    print("3. LinkedIn")

    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        role = input("Enter the job role: ")
        glassdoor_data(role)
        print("Glassdoor data saved to Data/glassdoor.json")
    elif choice == '2':
        role = input("Enter the job role: ")
        indeed_data(role)
        print("Indeed data saved to Data/indeed.json")
    elif choice == '3':
        role = input("Enter the job role: ")
        location = input("Enter the location: ")
        get_linkedin_jobs(role, location)
        print("LinkedIn data saved to Data/linkedin_jobs.json")
    else:
        print("Invalid choice. Please enter a number between 1 and 3.")

if __name__ == '__main__':
    main()
