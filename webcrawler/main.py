from core.verification_engine import verify_person

if __name__ == "__main__":
    name = input("Enter person's name: ")
    npi = input("Enter NPI (optional): ")

    print(verify_person(name, npi))


# eg names : Male Names
# Ethan Miller
# Jacob Anderson
# Michael Thompson
# Daniel Harris
# Ryan Walker
# Female Names
# Emily Parker
# Sophia Bennett
# Olivia Carter
# Madison Lewis
# Grace Mitchell 