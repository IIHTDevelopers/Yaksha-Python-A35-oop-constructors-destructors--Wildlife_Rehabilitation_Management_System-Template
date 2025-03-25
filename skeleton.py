"""
Wildlife Rehabilitation Management System

This module implements a wildlife rehabilitation center management system
focusing on constructors and destructors for resource management.

TODO: Implement all the classes and methods following the specifications
"""

import datetime


class Animal:
    """Class representing a wildlife patient."""
    
    animal_count = 0  # Class variable to track total animals
    
    def __init__(self, animal_id, species, condition, intake_date):
        """
        Initialize an Animal object with required tracking information.
        
        Args:
            animal_id: Unique identifier for the animal
            species: Species of the animal
            condition: Health condition or reason for admission
            intake_date: Date the animal was brought in (YYYY-MM-DD)
        
        TODO:
        - Validate parameters (animal_id must be a non-empty string)
        - Initialize instance attributes with double underscore prefix for private attributes
          (animal_id, species, condition, intake_date, discharge_date, assigned_enclosure, status)
        - Set discharge_date to None
        - Set assigned_enclosure to None
        - Set status to "In rehabilitation"
        - Increment animal_count class variable
        """
        # WRITE YOUR CODE HERE
        pass
    
    def __del__(self):
        """
        Clean up animal resources when the object is destroyed.
        
        TODO:
        - Check if animal was properly discharged, and if not, set discharge_date to current date
        - Decrement animal_count class variable
        """
        # WRITE YOUR CODE HERE
        pass
    
    # TODO: Implement property getters and setters for:
    # animal_id, species, condition, status, assigned_enclosure
    
    def discharge(self, discharge_date, status):
        """
        Discharge the animal from rehabilitation.
        
        Args:
            discharge_date: Date of discharge (YYYY-MM-DD)
            status: Final status (Released, Transferred, Euthanized, etc.)
            
        TODO:
        - Update the animal's discharge_date
        - Update the animal's status
        - Do NOT set assigned_enclosure to None here (let the RehabilitationCenter handle this)
        - Return True
        """
        # WRITE YOUR CODE HERE
        pass
    
    def display_info(self):
        """
        Display animal information.
        
        Returns:
            str: Formatted string with animal information
        
        TODO:
        - Return a formatted string containing animal_id, species, condition, and status
        """
        # WRITE YOUR CODE HERE
        pass


class Enclosure:
    """Class representing an animal enclosure at the rehabilitation center."""
    
    enclosure_count = 0  # Class variable to track total enclosures
    
    def __init__(self, enclosure_id, enclosure_type, capacity):
        """
        Initialize an Enclosure object with required attributes.
        
        Args:
            enclosure_id: Unique identifier for the enclosure
            enclosure_type: Type of enclosure (Aviary, Aquatic, Mammal, etc.)
            capacity: Maximum number of animals the enclosure can hold
            
        TODO:
        - Validate parameters (capacity must be a positive integer)
        - Initialize instance attributes with double underscore prefix
          (enclosure_id, enclosure_type, capacity, animals, is_active)
        - Set animals to an empty list
        - Set is_active to True
        - Increment enclosure_count class variable
        """
        # WRITE YOUR CODE HERE
        pass
    
    def __del__(self):
        """
        Clean up enclosure resources when the object is destroyed.
        
        TODO:
        - Check if enclosure still has animals and clear the animals list
        - Set is_active to False
        - Decrement enclosure_count class variable
        """
        # WRITE YOUR CODE HERE
        pass
    
    # TODO: Implement property getters for:
    # enclosure_id, enclosure_type, capacity, animals, available_capacity
    # NOTE: animals property must return a COPY of the list to ensure immutability
    
    def add_animal(self, animal_id):
        """
        Add an animal to this enclosure if space is available.
        
        Args:
            animal_id: ID of the animal to add
            
        Returns:
            bool: True if addition successful, False otherwise
            
        TODO:
        - Check if enclosure is at capacity, and if so, return False
        - Check if animal is already in the enclosure, and if not, add it
        - Return True if the animal was added, False otherwise
        """
        # WRITE YOUR CODE HERE
        pass
    
    def remove_animal(self, animal_id):
        """
        Remove an animal from this enclosure.
        
        Args:
            animal_id: ID of the animal to remove
            
        Returns:
            bool: True if removal successful, False otherwise
            
        TODO:
        - Check if animal is in the enclosure, and if so, remove it
        - Return True if the animal was removed, False otherwise
        """
        # WRITE YOUR CODE HERE
        pass
    
    def display_info(self):
        """
        Display enclosure information.
        
        Returns:
            str: Formatted string with enclosure information
            
        TODO:
        - Return a formatted string containing enclosure_id, enclosure_type, and current/total capacity
        """
        # WRITE YOUR CODE HERE
        pass


class RehabilitationCenter:
    """Class representing the wildlife rehabilitation center."""
    
    def __init__(self, name, location):
        """
        Initialize a RehabilitationCenter object with required attributes.
        
        Args:
            name: Name of the rehabilitation center
            location: Location of the rehabilitation center
            
        TODO:
        - Validate parameters (name must be a non-empty string)
        - Initialize instance attributes with double underscore prefix
          (name, location, animals, enclosures, system_start_time)
        - Set animals and enclosures to empty dictionaries
        - Set system_start_time to the current datetime
        """
        # WRITE YOUR CODE HERE
        pass
    
    def __del__(self):
        """
        Clean up center resources when the object is destroyed.
        
        TODO:
        - Calculate runtime statistics (days and hours) 
        - Clear all collections (animals and enclosures)
        """
        # WRITE YOUR CODE HERE
        pass
    
    # TODO: Implement property getters for:
    # name, location, animal_count, enclosure_count
    
    def add_animal(self, animal):
        """
        Add an animal to the center.
        
        Args:
            animal: Animal object to add
            
        Returns:
            bool: True if addition successful, False otherwise
            
        TODO:
        - Check if animal already exists, and if so, return False
        - Add the animal to the animals dictionary
        - Return True if the animal was added
        """
        # WRITE YOUR CODE HERE
        pass
    
    def get_animal(self, animal_id):
        """
        Get an animal by ID.
        
        Args:
            animal_id: ID of the animal to get
            
        Returns:
            Animal: Animal object if found, None otherwise
            
        TODO:
        - Return the animal from the animals dictionary or None if not found
        """
        # WRITE YOUR CODE HERE
        pass
    
    def discharge_animal(self, animal_id, discharge_date, status):
        """
        Discharge an animal from the center.
        
        Args:
            animal_id: ID of the animal to discharge
            discharge_date: Date of discharge (YYYY-MM-DD)
            status: Final status (Released, Transferred, Euthanized, etc.)
            
        Returns:
            bool: True if discharge successful, False otherwise
            
        TODO:
        - Get the animal by ID, and if not found, return False
        - Store the enclosure ID before updating animal status
        - If the animal is assigned to an enclosure, remove it from the enclosure
        - Update the animal's status by calling its discharge method
        - Set the animal's assigned_enclosure to None
        - Return True if the animal was discharged
        """
        # WRITE YOUR CODE HERE
        pass
    
    def add_enclosure(self, enclosure):
        """
        Add an enclosure to the center.
        
        Args:
            enclosure: Enclosure object to add
            
        Returns:
            bool: True if addition successful, False otherwise
            
        TODO:
        - Check if enclosure already exists, and if so, return False
        - Add the enclosure to the enclosures dictionary
        - Return True if the enclosure was added
        """
        # WRITE YOUR CODE HERE
        pass
    
    def get_enclosure(self, enclosure_id):
        """
        Get an enclosure by ID.
        
        Args:
            enclosure_id: ID of the enclosure to get
            
        Returns:
            Enclosure: Enclosure object if found, None otherwise
            
        TODO:
        - Return the enclosure from the enclosures dictionary or None if not found
        """
        # WRITE YOUR CODE HERE
        pass
    
    def assign_animal_to_enclosure(self, animal_id, enclosure_id):
        """
        Assign an animal to an enclosure.
        
        Args:
            animal_id: ID of the animal to assign
            enclosure_id: ID of the enclosure to assign the animal to
            
        Returns:
            bool: True if assignment successful, False otherwise
            
        TODO:
        - Get the animal and enclosure by ID, and if either not found, return False
        - If the animal is already assigned to an enclosure, remove it from that enclosure
        - Add the animal to the new enclosure and update the animal's assigned_enclosure
        - Return True if the assignment was successful
        """
        # WRITE YOUR CODE HERE
        pass


def main():
    """Main function to run the wildlife rehabilitation management system."""
    # TODO: Implement the main function to demonstrate your classes
    # HINT: Create a center, add enclosures and animals, and implement a menu-driven interface
    # WRITE YOUR CODE HERE
    pass


if __name__ == "__main__":
    main()