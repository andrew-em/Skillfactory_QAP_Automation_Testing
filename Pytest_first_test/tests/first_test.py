import pytest
from app.calculator import Calculator

class TestCalc:
   def setup(self):
       self.calc = Calculator

   def test_multiply_correctly(self):
       assert self.calc.multiply(self, 2, 2) == 4

   def test_multiply_failed(self):
       assert self.calc.multiply(self, 2, 2) == 5

   def test_division_correctly(self):
       assert self.calc.division(self, 8, 2) == 4

   def test_division_failed(self):
       assert self.calc.division(self, 8, 2) == 5

   def test_subtraction_correctly(self):
       assert self.calc.subtaction(self, 6, 2) == 4

   def test_subtraction_failed(self):
       assert self.calc.subtraction(self, 6, 2) == 5

   def test_adding_correctly(self):
       assert self.calc.adding(self, 2, 2) == 4

   def test_adding_failed(self):
       assert self.calc.adding(self, 2, 2) == 5