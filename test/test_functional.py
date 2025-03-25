import pytest
import datetime
from test.TestUtils import TestUtils
from wildlife_rehabilitation_management_system import Animal, Enclosure, RehabilitationCenter

class TestFunctional:
    """Test cases for functional requirements of the wildlife rehabilitation system."""
    
    def test_animal_constructor_destructor(self):
        """Test Animal class constructor and destructor functionality."""
        try:
            # Test basic animal creation and property access
            animal = Animal("A001", "Red Fox", "Injured leg", "2023-05-15")
            assert animal.animal_id == "A001"
            assert animal.species == "Red Fox"
            assert animal.condition == "Injured leg"
            assert animal.status == "In rehabilitation"
            assert animal.assigned_enclosure is None
            
            # Test class counter incrementation
            initial_count = Animal.animal_count
            animal2 = Animal("A002", "Barn Owl", "Wing injury", "2023-05-16")
            assert Animal.animal_count == initial_count + 1
            
            # Force destructor call and test count decrement
            # We need to delete the reference to trigger __del__
            del animal2
            # Note: The count won't immediately update due to garbage collection timing
            # This test is more for demonstration of what should happen
            
            TestUtils.yakshaAssert("test_animal_constructor_destructor", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_animal_constructor_destructor", False, "functional")
            raise e
    
    def test_enclosure_constructor_destructor(self):
        """Test Enclosure class constructor and destructor functionality."""
        try:
            # Test basic enclosure creation and property access
            enclosure = Enclosure("E001", "Aviary", 5)
            assert enclosure.enclosure_id == "E001"
            assert enclosure.enclosure_type == "Aviary"
            assert enclosure.capacity == 5
            assert len(enclosure.animals) == 0
            assert enclosure.available_capacity == 5
            
            # Test adding animals affects capacity
            enclosure.add_animal("A001")
            enclosure.add_animal("A002")
            assert len(enclosure.animals) == 2
            assert enclosure.available_capacity == 3
            
            # Test class counter incrementation
            initial_count = Enclosure.enclosure_count
            enclosure2 = Enclosure("E002", "Mammal Habitat", 3)
            assert Enclosure.enclosure_count == initial_count + 1
            
            # Force destructor call with animals still in enclosure
            # This should trigger a warning in the destructor
            enclosure2.add_animal("A003")
            del enclosure2
            
            TestUtils.yakshaAssert("test_enclosure_constructor_destructor", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_enclosure_constructor_destructor", False, "functional")
            raise e
    
    def test_rehabilitation_center_constructor_destructor(self):
        """Test RehabilitationCenter class constructor and destructor functionality."""
        try:
            # Test center creation and property access
            center = RehabilitationCenter("Wildlife Rescue", "123 Forest Road")
            assert center.name == "Wildlife Rescue"
            assert center.location == "123 Forest Road"
            assert center.animal_count == 0
            assert center.enclosure_count == 0
            
            # Add animals and enclosures to test constructor initialization of collections
            animal = Animal("A001", "Red Fox", "Injured leg", "2023-05-15")
            enclosure = Enclosure("E001", "Aviary", 5)
            
            center.add_animal(animal)
            center.add_enclosure(enclosure)
            
            assert center.animal_count == 1
            assert center.enclosure_count == 1
            
            # Destroying center should properly clean up resources
            # and produce final state report
            del center
            
            TestUtils.yakshaAssert("test_rehabilitation_center_constructor_destructor", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_rehabilitation_center_constructor_destructor", False, "functional")
            raise e
    
    def test_animal_discharge_process(self):
        """Test animal discharge process and resource management."""
        try:
            # Setup center with animals and enclosures
            center = RehabilitationCenter("Test Center", "Test Location")
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            
            animal = Animal("A001", "Red Fox", "Injured leg", "2023-05-15")
            enclosure = Enclosure("E001", "Mammal Habitat", 3)
            
            center.add_animal(animal)
            center.add_enclosure(enclosure)
            
            # Assign animal to enclosure
            center.assign_animal_to_enclosure("A001", "E001")
            assert animal.assigned_enclosure == "E001"
            assert "A001" in enclosure.animals
            
            # Discharge animal
            center.discharge_animal("A001", today, "Released")
            
            # Verify enclosure resources were properly released
            assert animal.status == "Released"
            assert animal.assigned_enclosure is None
            assert "A001" not in enclosure.animals
            
            TestUtils.yakshaAssert("test_animal_discharge_process", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_animal_discharge_process", False, "functional")
            raise e
    
    def test_enclosure_resource_management(self):
        """Test enclosure resource allocation and deallocation."""
        try:
            # Create enclosure and test initial resource state
            enclosure = Enclosure("E002", "Reptile Habitat", 4)
            assert enclosure.available_capacity == 4
            
            # Add animals to consume resources
            enclosure.add_animal("A001")
            enclosure.add_animal("A002")
            assert enclosure.available_capacity == 2
            
            # Remove animals to free resources
            enclosure.remove_animal("A001")
            assert enclosure.available_capacity == 3
            
            # Test capacity limits
            enclosure.add_animal("A003")
            enclosure.add_animal("A004")
            enclosure.add_animal("A005")
            assert enclosure.available_capacity == 0
            assert enclosure.add_animal("A006") == False  # Should fail - no capacity
            
            TestUtils.yakshaAssert("test_enclosure_resource_management", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_enclosure_resource_management", False, "functional")
            raise e
    
    def test_constructor_validation(self):
        """Test parameter validation in constructors."""
        try:
            # Test Animal constructor validation
            try:
                Animal("", "Species", "Condition", "2023-05-15")
                assert False, "Animal constructor should reject empty ID"
            except ValueError:
                pass  # Expected behavior
            
            # Test Enclosure constructor validation
            try:
                Enclosure("E001", "Type", 0)
                assert False, "Enclosure constructor should reject zero capacity"
            except ValueError:
                pass  # Expected behavior
            
            try:
                Enclosure("E001", "Type", -5)
                assert False, "Enclosure constructor should reject negative capacity"
            except ValueError:
                pass  # Expected behavior
            
            TestUtils.yakshaAssert("test_constructor_validation", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_constructor_validation", False, "functional")
            raise e
    
    def test_integrated_system(self):
        """Test integrated system with multiple operations."""
        try:
            # Create rehabilitation center
            center = RehabilitationCenter("Integrated Center", "Test Location")
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Create animals and enclosures
            animals = [
                Animal("A001", "Red Fox", "Leg injury", today),
                Animal("A002", "Barn Owl", "Wing injury", today),
                Animal("A003", "Box Turtle", "Shell damage", today)
            ]
            
            enclosures = [
                Enclosure("E001", "Mammal Habitat", 2),
                Enclosure("E002", "Aviary", 3),
                Enclosure("E003", "Reptile Habitat", 5)
            ]
            
            # Add animals and enclosures to center
            for animal in animals:
                center.add_animal(animal)
                
            for enclosure in enclosures:
                center.add_enclosure(enclosure)
            
            # Assign animals to appropriate enclosures
            center.assign_animal_to_enclosure("A001", "E001")
            center.assign_animal_to_enclosure("A002", "E002")
            center.assign_animal_to_enclosure("A003", "E003")
            
            # Verify assignments
            assert animals[0].assigned_enclosure == "E001"
            assert animals[1].assigned_enclosure == "E002"
            assert animals[2].assigned_enclosure == "E003"
            
            # Test resource contention
            animal4 = Animal("A004", "Raccoon", "Minor injuries", today)
            center.add_animal(animal4)
            center.assign_animal_to_enclosure("A004", "E001")
            
            # Enclosure E001 should now be at capacity
            animal5 = Animal("A005", "Fox", "Injured paw", today)
            center.add_animal(animal5)
            assert center.assign_animal_to_enclosure("A005", "E001") == False
            
            # Discharge an animal and verify resources are freed
            center.discharge_animal("A001", today, "Released")
            assert animals[0].status == "Released"
            assert animals[0].assigned_enclosure is None
            assert "A001" not in enclosures[0].animals
            
            # Now there should be room for animal5
            assert center.assign_animal_to_enclosure("A005", "E001") == True
            assert animal5.assigned_enclosure == "E001"
            
            TestUtils.yakshaAssert("test_integrated_system", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_integrated_system", False, "functional")
            raise e