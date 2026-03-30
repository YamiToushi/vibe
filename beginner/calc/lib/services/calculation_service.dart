class CalculationService {
  static double calculate(double first, double second, String operator) {
    switch (operator) {
      case '+':
        return first + second;
      case '-':
        return first - second;
      case '×':
        return first * second;
      case '÷':
        if (second == 0) {
          // Handle division by zero with exception
          throw Exception('Division by zero');
        }
        return first / second;
      default:
        return second;
    }
  }
}