import pytest
import datetime
from test.TestUtils import TestUtils
from wildlife_rehabilitation_management_system import Animal, Enclosure, RehabilitationCenter

class TestExceptional:
    """Test cases for exceptional conditions in the wildlife rehabilitation system."""
    
    def test_exception_handling(self):
        """Test all exception handling across the wildlife rehabilitation system."""
        try:
            # Animal validation exceptions
            try:
                Animal("", "Species", "Condition", "2023-06-01")
                assert False, "Empty animal_id should be rejected"
            except ValueError:
                pass  # Expected behavior
                
            try:
                Animal(123, "Species", "Condition", "2023-06-01")
                assert False, "Non-string animal_id should be rejected"
            except ValueError:
                pass  # Expected behavior
            
            # Enclosure validation exceptions
            try:
                Enclosure("E001", "Type", -1)
                assert False, "Negative capacity should be rejected"
            except ValueError:
                pass  # Expected behavior
                
            try:
                Enclosure("E001", "Type", 0)
                assert False, "Zero capacity should be rejected"
            except ValueError:
                pass  # Expected behavior
                
            try:
                Enclosure("E001", "Type", "5")
                assert False, "Non-integer capacity should be rejected"
            except ValueError:
                pass  # Expected behavior
            
            # Animal already exists exception
            center = RehabilitationCenter("Test Center", "Test Location")
            animal = Animal("A001", "Species", "Condition", "2023-06-01")
            
            assert center.add_animal(animal) is True
            assert center.add_animal(animal) is False, "Adding duplicate animal should return False"
            
            # Enclosure already exists exception
            enclosure = Enclosure("E001", "Type", 5)
            
            assert center.add_enclosure(enclosure) is True
            assert center.add_enclosure(enclosure) is False, "Adding duplicate enclosure should return False"
            
            # Add animal to full enclosure
            full_enclosure = Enclosure("E002", "Small", 1)
            center.add_enclosure(full_enclosure)
            
            animal1 = Animal("A002", "Species", "Condition", "2023-06-01")
            animal2 = Animal("A003", "Species", "Condition", "2023-06-01")
            center.add_animal(animal1)
            center.add_animal(animal2)
            
            assert full_enclosure.add_animal("A002") is True
            assert full_enclosure.add_animal("A003") is False, "Adding animal to full enclosure should fail"
            
            # Remove non-existent animal from enclosure
            assert full_enclosure.remove_animal("NONEXISTENT") is False, "Removing non-existent animal should fail"
            
            # Discharge non-existent animal
            assert center.discharge_animal("NONEXISTENT", "2023-06-01", "Released") is False, "Discharging non-existent animal should fail"
            
            # Assignment exceptions
            # Assign to non-existent enclosure
            assert center.assign_animal_to_enclosure("A001", "NONEXISTENT") is False, "Assigning to non-existent enclosure should fail"
            
            # Assign non-existent animal
            assert center.assign_animal_to_enclosure("NONEXISTENT", "E001") is False, "Assigning non-existent animal should fail"
            
            # Edge case: Animal already discharged
            discharged_animal = Animal("A004", "Species", "Condition", "2023-06-01")
            center.add_animal(discharged_animal)
            center.discharge_animal("A004", "2023-06-01", "Released")
            
            # Try to assign discharged animal
            assert center.assign_animal_to_enclosure("A004", "E001") is True, "Should be able to assign discharged animal"
            assert discharged_animal.assigned_enclosure == "E001", "Discharged animal's enclosure should be updated"
            
            # Try to remove animal from enclosure when not in any
            isolated_animal = Animal("A005", "Species", "Condition", "2023-06-01")
            assert isolated_animal.assigned_enclosure is None
            
            # Constructor validation
            try:
                RehabilitationCenter(123, "Location")
                assert False, "Non-string center name should be rejected"
            except ValueError:
                pass  # Expected behavior
                
            try:
                RehabilitationCenter("", "Location")
                assert False, "Empty center name should be rejected"
            except ValueError:
                pass  # Expected behavior
                
            TestUtils.yakshaAssert("test_exception_handling", True, "exceptional")
        except Exception as e:
            TestUtils.yakshaAssert("test_exception_handling", False, "exceptional")
            raise e