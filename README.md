# Testing with Python

This repository mostly covers ways to test Python applications using boto3 but also
uses best practices for testing in general.

# MagicMock

### Pros

 - Already part of python 3.3+
 - Well documented
 - Support for mocking anything you want
   - Most mock libraries will extend mock for easier use
 - "Pythonic" way of monkeypatching objects for tests

### Cons

 - Verbose
 - You write a lot of boilerplate

# Moto

### Pros

 - Easy to use (just works)
 - Good docs
 - Flexible
 - Remembers state about your current test
   - Ability to verify that "created" object exists
 - Easily mock multiple API calls

### Cons

 - A lot of services are unsupported

> Adding support isn't difficult. But the project doesn't have a ton of support

# Placebo

### Pros

 -

### Cons

 -

# Stubber

### Pros

 - Included with botocore
 - Simple to use

### Cons

 - Verbose
 - You will write a lot of boilerplate
 - Requires dependency injection

