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
 - Use with dependency injection

### Cons

 - Verbose
 - You write a lot of boilerplate

## Thoughts

This is honestly my favorite way to write tests. It requires a bit of
boilerplate that could be easily abstracted to a module or just rewritten
for every project and shared across tests.

There's nothing MagickMock can't do that I've found while testing.

# Moto

### Pros

 - Easy to use (just works*)
 - Easily mock multiple API calls
 - Similar to just using boto3 directly - low learning curve

### Cons

 - A lot of services are unsupported
 - No or little ability to force exceptions or negative tests currently

> Adding support isn't difficult. But the project doesn't have a ton of support

> * When it works, it works. But there are many gaps

## Thoughts

I love the idea behind moto. Given its smaller lack of adoption though and the amount of missing services I find it hard to endorse. I hope to see this project continue though because it has the potential to be the best option for testing AWS services since it's stateful and never requires calls to AWS to set it up.

# Placebo

### Pros

 - Super simple to use *
 - Write tests quickly
 - "Pythonic" way of monkeypatching objects for tests
 - Great for figuring out how to mock responses in general

> * So simple I was confused by how to even set it up

### Cons

 - No ability to use with Dependency Injection *
 - Requires making actual API calls to use ( No TDD with this lib )
 - No obvious support for exceptions **
 - Potentially **LEAKED SECRETS**

> * There's likely a way since you're patching the session - it's just not obvious or documented

> ** There probably is a way to modify the response files to cause exceptions

## Thoughts

This tools is super interesting and I like the idea of how it works. However, the lack of TDD, poor documentation, and "magic" of it working leaves a lot to be desired.

I used this tool to generate an IoT thing certificate and it logs every response to disk. My certificate pem and private key were put on disk. If I committed this to be used for tests in the future without checking the file I could have committed a valid certificate to source control.

# Stubber

### Pros

 - Included with botocore
 - Simple to use
 - Combine with patch for "Pythonic" way of monkeypatching objects for tests
 - Use with dependency injection
 - Test expected parameters

### Cons

 - Verbose
 - Requires dependency injection
 - No ability to support exceptions or errors*
 - Does not support [resources](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html) or Paginators

> * Could not figure out how to raise exceptions

## Thoughts

This is my second favorite method of mocking boto3 calls. It's easier to use (less boilerplate) than Magic Mock but also a little harder to do things like force exceptions and test failure cases.
