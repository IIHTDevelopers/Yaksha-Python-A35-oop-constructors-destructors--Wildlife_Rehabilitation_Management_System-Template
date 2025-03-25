import pytest
import datetime
from test.TestUtils import TestUtils
from wildlife_rehabilitation_management_system import Animal, Enclosure, RehabilitationCenter

class TestBoundary:
    """Test cases for boundary conditions in the wildlife rehabilitation system."""
    
    def test_system_boundaries(self):
        """Test all boundary conditions for the wildlife rehabilitation system."""
        try:
            # Animal boundary tests
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            animal1 = Animal("A001", "Red Fox", "Minor injury", today)
            assert animal1.animal_id == "A001"
            assert animal1.species == "Red Fox"
            
            animal2 = Animal("A002", "Bald Eagle", "Severe wing injury", today)
            assert animal2.status == "In rehabilitation"
            
            animal3 = Animal("A003", "Box Turtle", "Shell damage", today)
            assert animal3.assigned_enclosure is None
            
            # Enclosure capacity boundary tests
            enclosure = Enclosure("E001", "Aviary", 3)
            assert enclosure.capacity == 3
            assert enclosure.available_capacity == 3
            
            # Add animals up to capacity
            animals = [
                Animal(f"A00{i}", f"Animal {i}", "Condition", today) 
                for i in range(4, 7)
            ]
            
            for i in range(3):
                assert enclosure.add_animal(animals[i].animal_id) == True
            
            # Test capacity limit
            assert enclosure.available_capacity == 0
            assert enclosure.add_animal("A007") == False
            
            # Test removal to free capacity
            assert enclosure.remove_animal(animals[0].animal_id) == True
            assert enclosure.available_capacity == 1
            assert enclosure.add_animal("A007") == True
            
            # Test animals list immutability
            enclosure_animals = enclosure.animals
            enclosure_animals.append("A008")
            assert "A008" not in enclosure.animals
            
            # Empty center tests
            center = RehabilitationCenter("Empty Center", "Nowhere")
            assert center.animal_count == 0
            assert center.enclosure_count == 0
            assert center.get_animal("A001") is None
            assert center.get_enclosure("E001") is None
            
            # Center assignment tests
            test_center = RehabilitationCenter("Test Center", "Test Location")
            test_animal = Animal("A001", "Wolf", "Leg injury", today)
            test_enclosure = Enclosure("E001", "Mammal Habitat", 5)
            
            test_center.add_animal(test_animal)
            test_center.add_enclosure(test_enclosure)
            
            # Test invalid assignments
            assert test_center.assign_animal_to_enclosure("INVALID", "E001") is False
            assert test_center.assign_animal_to_enclosure("A001", "INVALID") is False
            
            # Valid assignment and reassignment test
            assert test_center.assign_animal_to_enclosure("A001", "E001") is True
            assert test_animal.assigned_enclosure == "E001"
            
            # Create second enclosure and test reassignment
            test_enclosure2 = Enclosure("E002", "Recovery Area", 3)
            test_center.add_enclosure(test_enclosure2)
            
            assert test_center.assign_animal_to_enclosure("A001", "E002") is True
            assert test_animal.assigned_enclosure == "E002"
            assert "A001" not in test_enclosure.animals
            
            # Discharge tests
            assert test_center.discharge_animal("A001", today, "Released") is True
            assert test_animal.status == "Released"
            assert test_animal.assigned_enclosure is None
            assert "A001" not in test_enclosure2.animals
            
            TestUtils.yakshaAssert("test_system_boundaries", True, "boundary")
        except Exception as e:
            TestUtils.yakshaAssert("test_system_boundaries", False, "boundary")
            raise e