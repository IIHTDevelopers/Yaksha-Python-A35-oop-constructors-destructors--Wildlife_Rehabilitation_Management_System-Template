"""
Wildlife Rehabilitation Management System

This module implements a wildlife rehabilitation center management system
focusing on constructors and destructors for resource management.
"""

import datetime


class Animal:
    """Class representing a wildlife patient."""
    
    animal_count = 0
    
    def __init__(self, animal_id, species, condition, intake_date):
        """Initialize an Animal object with required tracking information."""
        # Validate parameters
        if not isinstance(animal_id, str) or not animal_id:
            raise ValueError("Animal ID must be a non-empty string")
        
        # Initialize attributes
        self.__animal_id = animal_id
        self.__species = species
        self.__condition = condition
        self.__intake_date = intake_date
        self.__discharge_date = None
        self.__assigned_enclosure = None
        self.__status = "In rehabilitation"
        
        # Increment animal count
        Animal.animal_count += 1
    
    def __del__(self):
        """Clean up animal resources when the object is destroyed."""
        # Check if animal was properly discharged
        if self.__discharge_date is None:
            self.__discharge_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Decrement animal count
        Animal.animal_count -= 1
    
    @property
    def animal_id(self): return self.__animal_id
    
    @property
    def species(self): return self.__species
    
    @property
    def condition(self): return self.__condition
    
    @property
    def status(self): return self.__status
    
    @property
    def assigned_enclosure(self): return self.__assigned_enclosure
    
    @assigned_enclosure.setter
    def assigned_enclosure(self, enclosure_id): 
        self.__assigned_enclosure = enclosure_id
    
    def discharge(self, discharge_date, status):
        """Discharge the animal from rehabilitation."""
        self.__discharge_date = discharge_date
        self.__status = status
        return True
    
    def display_info(self):
        """Display animal information."""
        return f"{self.__animal_id} | {self.__species} | {self.__condition} | Status: {self.__status}"


class Enclosure:
    """Class representing an animal enclosure at the rehabilitation center."""
    
    enclosure_count = 0
    
    def __init__(self, enclosure_id, enclosure_type, capacity):
        """Initialize an Enclosure object with required attributes."""
        # Validate parameters
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        
        # Initialize attributes
        self.__enclosure_id = enclosure_id
        self.__enclosure_type = enclosure_type
        self.__capacity = capacity
        self.__animals = []
        self.__is_active = True
        
        # Increment enclosure count
        Enclosure.enclosure_count += 1
    
    def __del__(self):
        """Clean up enclosure resources when the object is destroyed."""
        # Clear animals and release resources
        self.__animals.clear()
        self.__is_active = False
        
        # Decrement enclosure count
        Enclosure.enclosure_count -= 1
    
    @property
    def enclosure_id(self): return self.__enclosure_id
    
    @property
    def enclosure_type(self): return self.__enclosure_type
    
    @property
    def capacity(self): return self.__capacity
    
    @property
    def animals(self): return self.__animals.copy()
    
    @property
    def available_capacity(self): return self.__capacity - len(self.__animals)
    
    def add_animal(self, animal_id):
        """Add an animal to this enclosure if space is available."""
        if len(self.__animals) >= self.__capacity:
            return False
        
        if animal_id not in self.__animals:
            self.__animals.append(animal_id)
            return True
        
        return False
    
    def remove_animal(self, animal_id):
        """Remove an animal from this enclosure."""
        if animal_id in self.__animals:
            self.__animals.remove(animal_id)
            return True
        
        return False
    
    def display_info(self):
        """Display enclosure information."""
        return f"{self.__enclosure_id} | {self.__enclosure_type} | Capacity: {len(self.__animals)}/{self.__capacity}"


class RehabilitationCenter:
    """Class representing the wildlife rehabilitation center."""
    
    def __init__(self, name, location):
        """Initialize a RehabilitationCenter object with required attributes."""
        # Validate parameters
        if not isinstance(name, str) or not name:
            raise ValueError("Center name must be a non-empty string")
            
        # Initialize attributes
        self.__name = name
        self.__location = location
        self.__animals = {}
        self.__enclosures = {}
        self.__system_start_time = datetime.datetime.now()
    
    def __del__(self):
        """Clean up center resources when the object is destroyed."""
        # Clear all collections
        self.__animals.clear()
        self.__enclosures.clear()
    
    @property
    def name(self): return self.__name
    
    @property
    def location(self): return self.__location
    
    @property
    def animal_count(self): return len(self.__animals)
    
    @property
    def enclosure_count(self): return len(self.__enclosures)
    
    # Animal management methods
    def add_animal(self, animal):
        """Add an animal to the center."""
        if animal.animal_id in self.__animals:
            return False
        
        self.__animals[animal.animal_id] = animal
        return True
    
    def get_animal(self, animal_id):
        """Get an animal by ID."""
        return self.__animals.get(animal_id)
    
    def discharge_animal(self, animal_id, discharge_date, status):
        """Discharge an animal from the center."""
        animal = self.__animals.get(animal_id)
        if not animal:
            return False
        
        # Store the enclosure ID before updating animal status
        enclosure_id = animal.assigned_enclosure
        
        # Remove from enclosure if assigned
        if enclosure_id:
            enclosure = self.__enclosures.get(enclosure_id)
            if enclosure:
                enclosure.remove_animal(animal_id)
        
        # Update animal status after removing from enclosure
        animal.discharge(discharge_date, status)
        
        # Set assigned_enclosure to None after discharge and removal
        animal.assigned_enclosure = None
        
        return True
    
    # Enclosure management methods
    def add_enclosure(self, enclosure):
        """Add an enclosure to the center."""
        if enclosure.enclosure_id in self.__enclosures:
            return False
        
        self.__enclosures[enclosure.enclosure_id] = enclosure
        return True
    
    def get_enclosure(self, enclosure_id):
        """Get an enclosure by ID."""
        return self.__enclosures.get(enclosure_id)
    
    def assign_animal_to_enclosure(self, animal_id, enclosure_id):
        """Assign an animal to an enclosure."""
        animal = self.__animals.get(animal_id)
        enclosure = self.__enclosures.get(enclosure_id)
        
        if not animal or not enclosure:
            return False
        
        # Check if animal is already in another enclosure
        if animal.assigned_enclosure:
            old_enclosure = self.__enclosures.get(animal.assigned_enclosure)
            if old_enclosure:
                old_enclosure.remove_animal(animal_id)
        
        # Assign to new enclosure
        if enclosure.add_animal(animal_id):
            animal.assigned_enclosure = enclosure_id
            return True
        
        return False


def main():
    # Create the rehabilitation center
    center = RehabilitationCenter("WRA Wildlife Center", "123 Forest Road, Greenville")
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Create enclosures
    enclosures = [
        Enclosure("E001", "Aviary", 5),
        Enclosure("E002", "Mammal Habitat", 3),
        Enclosure("E003", "Reptile Habitat", 8)
    ]
    for enclosure in enclosures:
        center.add_enclosure(enclosure)
    
    # Create animals
    animals = [
        Animal("A001", "Red Fox", "Injured leg", "2023-05-15"),
        Animal("A002", "Barn Owl", "Wing injury", "2023-05-20"),
        Animal("A003", "Box Turtle", "Shell damage", "2023-05-22")
    ]
    for animal in animals:
        center.add_animal(animal)
    
    # Assign animals to enclosures
    center.assign_animal_to_enclosure("A001", "E002")
    center.assign_animal_to_enclosure("A002", "E001")
    center.assign_animal_to_enclosure("A003", "E003")
    
    # Discharge an animal
    center.discharge_animal("A001", today, "Transferred to long-term care facility")
    
    # Menu-based interaction
    while True:
        print("\n===== WILDLIFE REHABILITATION MANAGEMENT SYSTEM =====")
        print(f"Center Name: {center.name}")
        print(f"Location: {center.location}")
        print(f"Animals: {center.animal_count} | Enclosures: {center.enclosure_count}")
        print("\nMenu:")
        print("1. View Animals")
        print("2. View Enclosures")
        print("3. Add New Animal")
        print("4. Discharge Animal")
        print("0. Exit")
        
        try:
            choice = int(input("\nEnter your choice (0-4): "))
            
            if choice == 1:
                print("\nCurrent Animals:")
                for animal_id, animal in center._RehabilitationCenter__animals.items():
                    print(animal.display_info())
            
            elif choice == 2:
                print("\nEnclosures:")
                for enclosure_id, enclosure in center._RehabilitationCenter__enclosures.items():
                    print(enclosure.display_info())
            
            elif choice == 3:
                animal_id = input("Enter animal ID: ")
                species = input("Enter species: ")
                condition = input("Enter condition: ")
                intake_date = datetime.datetime.now().strftime("%Y-%m-%d")
                
                animal = Animal(animal_id, species, condition, intake_date)
                if center.add_animal(animal):
                    print(f"Animal {animal_id} added successfully.")
                else:
                    print(f"Animal with ID {animal_id} already exists.")
            
            elif choice == 4:
                animal_id = input("Enter animal ID: ")
                status = input("Enter release status: ")
                discharge_date = datetime.datetime.now().strftime("%Y-%m-%d")
                
                if center.discharge_animal(animal_id, discharge_date, status):
                    print(f"Animal {animal_id} discharged successfully.")
                else:
                    print(f"Animal with ID {animal_id} not found or already discharged.")
            
            elif choice == 0:
                print("Thank you for using the Wildlife Rehabilitation Management System.")
                break
            
            else:
                print("Invalid choice. Please enter a number between 0 and 4.")
        
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()