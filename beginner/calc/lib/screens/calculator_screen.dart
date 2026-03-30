import 'package:flutter/material.dart';
import 'package:calculator_app/widgets/display_widget.dart';
import 'package:calculator_app/widgets/button_pad.dart';
import 'package:calculator_app/services/input_service.dart';
import 'package:calculator_app/services/calculation_service.dart';

class CalculatorScreen extends StatefulWidget {
  const CalculatorScreen({super.key});

  @override
  State<CalculatorScreen> createState() => _CalculatorScreenState();
}

class _CalculatorScreenState extends State<CalculatorScreen> {
  String _displayValue = '0';
  String? _operator;
  String? _previousValue;
  bool _isNewOperation = true;
  bool _hasError = false;

  void _handleInput(String input) {
    setState(() {
      // Handle clear functions
      if (input == 'C') {
        _displayValue = '0';
        _operator = null;
        _previousValue = null;
        _isNewOperation = true;
        _hasError = false;
        return;
      }

      if (input == 'CE') {
        _displayValue = '0';
        _hasError = false;
        return;
      }

      // Handle equals
      if (input == '=') {
        if (_operator != null && _previousValue != null && !_hasError) {
          try {
            final result = CalculationService.calculate(
              double.parse(_previousValue!),
              double.parse(_displayValue),
              _operator!,
            );
            _displayValue = result.toString();
            _operator = null;
            _previousValue = null;
            _isNewOperation = true;
          } on Exception catch (e) {
            // Handle division by zero error
            _displayValue = 'Error';
            _hasError = true;
            _operator = null;
            _previousValue = null;
          }
        }
        return;
      }

      // Handle sign change - delegate to InputService
      if (input == '+/-') {
        _displayValue = InputService.handleInput(_displayValue, input);
        _isNewOperation = false;
        return;
      }

      // Handle decimal point - delegate to InputService
      if (input == '.') {
        _displayValue = InputService.handleInput(_displayValue, input);
        _isNewOperation = false;
        return;
      }

      // Handle operators
      if (['+', '-', '×', '÷'].contains(input)) {
        if (_previousValue == null) {
          _previousValue = _displayValue;
        } else if (_operator != null) {
          try {
            final result = CalculationService.calculate(
              double.parse(_previousValue!),
              double.parse(_displayValue),
              _operator!,
            );
            _previousValue = result.toString();
            _displayValue = result.toString();
          } on Exception catch (e) {
            // Handle division by zero error
            _displayValue = 'Error';
            _hasError = true;
            _operator = null;
            _previousValue = null;
            _isNewOperation = true;
            return;
          }
        }
        _operator = input;
        _isNewOperation = true; // This was the bug - it should be true to clear the display
        return;
      }

      // Handle digit input
      if (_isNewOperation) {
        _displayValue = input;
        _isNewOperation = false;
      } else {
        // Delegate digit input to InputService for consistent handling
        _displayValue = InputService.handleInput(_displayValue, input);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF1A1A2E),
      body: SafeArea( // Added SafeArea here
        child: Column(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: DisplayWidget(
                  value: _displayValue,
                  operator: _operator,
                  previousValue: _previousValue,
                ),
              ),
            ),
            ButtonPad(
              onButtonPressed: _handleInput,
            ),
          ],
        ),
      ),
    );
  }
}