+++
date = '2025-04-15T12:43:02+02:00'
draft = false
title = 'Design Patterns in Go: Practical Examples'
tags = ['go', 'golang', 'design patterns', 'architecture']
categories = ['Programming', 'Go']
summary = 'Explore creational, structural, and behavioral design patterns in Go with clear explanations and code snippets.'
comments = true
ShowToc = true
TocOpen = true
image = 'banner.jpg'
+++

Design patterns are reusable solutions to common problems in software design. 

They provide a shared language for developers and encourage best practices in system architecture. 

In this article, we'll explore some of the most widely used design patterns in Go, grouped into three categories: creational, structural, and behavioral.

<div style="display: flex; justify-content: center;">
  <img src="banner.jpg" alt="Design Patterns in Go" style="max-width: 100%; height: auto;" />
</div>

---

## 🔧 Creational Patterns

1. 🔂 Singleton 

   Ensures a class has only one instance and provides a global point of access to it.

   > “When discussing which pattern to drop, we found that we still love them all. (Not really — I'm in favor of dropping Singleton. Its use is almost always a design smell.)”  
   > — *Erich Gamma, Design Patterns: Elements of Reusable Object-Oriented Software*

   While Singleton often gets a bad reputation, there are still valid use cases in Go:

   - ✅ You only want **one component in the system** (e.g., database repository, object factory)
   - ⏳ The object is **expensive to construct**, so you instantiate it only once
   - 🚫 You want to **prevent the creation of additional instances**
   - 💤 You want **lazy instantiation** (e.g. load config or connect to DB only when needed)

   Go makes this easy and thread-safe with `sync.Once`. To stay testable and modular, follow the **Dependency Inversion Principle (DIP)** — depend on interfaces, not concrete types.

   **Hint:** Singleton quite often breaks the **Dependency Inversion Principle**!

    ```go
    package singleton
    
    import (
        "sync"
    )
    
    var (
        instance *singleton
        once     sync.Once
    )

    type singleton struct{}
       
    func GetInstance() *singleton {
        once.Do(func() {
            instance = &singleton{}
    })
   
    return instance
    }
    ```
   
1. 🏭 Factory

    Creates objects without specifying the exact class.

    A **factory** helps simplify object creation when:

    - 🌀 Object creation logic becomes **too convoluted**
    - 🧱 A struct has **too many fields** that need to be correctly initialized
    - 💡 You want to **delegate creation logic** away from the calling code

    There are two flavors of factories in Go:

    - 🔧 **Factory function** (also called a `constructor`): a helper function to initialize struct instances
    - 🏗️ **Factory struct**: a dedicated struct responsible for managing object creation

    Unlike the Builder pattern, which is *piecewise*, the Factory creates the object **wholesale** — usually in one go.

    Here's a simple example using a factory function:

    ```go
    package factory

    type Shape interface {
    Draw() string
    }
    
    type Circle struct{}
    func (c Circle) Draw() string { return "Drawing Circle" }
    
    type Square struct{}
    func (s Square) Draw() string { return "Drawing Square" }
    
    func GetShape(shapeType string) Shape {
        switch shapeType {
        case "circle":
            return Circle{}
        case "square":
            return Square{}
        default:
            return nil
        }
    }
    ```

1. 🧱 Builder

   Separates the construction of a complex object from its representation.

   Not all objects are created equal:

   - ✅ Some are simple and can be created with a single constructor call
   - ⚠️ Others require **a lot of ceremony** to set up
   - 🧩 Factory functions with **10+ parameters** become hard to use and maintain

   When you want more flexibility and readability, use the **Builder pattern**.

   - 🛠️ A **Builder** is a separate component used to construct an object step-by-step
   - 🔄 It exposes a **fluent API** — each method returns the receiver (`*Builder`) to enable chaining
   - 🧠 In advanced designs, **different builders** can operate on **different facets** of the same object

   Here's an example:

    ```go
    package builder
    
    type Car struct {
        Engine string
        Wheels int
        Color  string
    }
    
    type CarBuilder struct {
        car Car
    }
    
    func (b *CarBuilder) SetEngine(engine string) *CarBuilder {
        b.car.Engine = engine
        return b
    }
    
    func (b *CarBuilder) SetWheels(wheels int) *CarBuilder {
        b.car.Wheels = wheels
        return b
    }
    
    func (b *CarBuilder) SetColor(color string) *CarBuilder {
        b.car.Color = color
        return b
    }
    
    func (b *CarBuilder) Build() Car {
        return b.car
    }
    ```

---

## 🧩 Structural Patterns

1. 🔌 Adapter

    Allows incompatible interfaces to work together.

    ```go
    package adapter
    
    type Target interface {
        Request() string
    }
    
    type Adaptee struct{}
        func (a Adaptee) SpecificRequest() string {
            return "Specific behavior"
    }
    
    type Adapter struct {
        adaptee Adaptee
    }
    
    func (a Adapter) Request() string {
        return a.adaptee.SpecificRequest()
    }
    ```

1. 🎀 Decorator

    Adds behavior to objects dynamically.

    ```go
    package decorator
    
    type Coffee interface {
        Cost() float64
    }
    
    type SimpleCoffee struct{}
        func (s SimpleCoffee) Cost() float64 { 
            return 2.0 
        }
    
    type MilkDecorator struct {
        Coffee
    }
    
    func (m MilkDecorator) Cost() float64 {
        return m.Coffee.Cost() + 0.5
    }
    ```

1. 🛡 Proxy

   Provides a surrogate or placeholder.

   ```go
    package proxy
    
    type Image interface {
        Display() string
    }
    
    type RealImage struct {
        filename string
    }
    
    func (r RealImage) Display() string {
        return "Displaying " + r.filename
    }
    
    type ProxyImage struct {
        realImage *RealImage
        filename  string
    }
    
    func (p *ProxyImage) Display() string {
        if p.realImage == nil {
        p.realImage = &RealImage{filename: p.filename}
        }
    
        return p.realImage.Display()
    }
   ```

1. 🌳 Composite

    Composes objects into tree structures.

    ```go
   package composite

    type Component interface {
        Operation() string
    }
    
    type Leaf struct {
        name string
    }
    
    func (l Leaf) Operation() string {
        return l.name
    }
    
    type Composite struct {
        children []Component
    }
    
    func (c *Composite) Add(child Component) {
        c.children = append(c.children, child)
    }
    
    func (c *Composite) Operation() string {
        result := ""
        for _, child := range c.children {
            result += child.Operation() + " "
        }
    
        return result
    }
    ```

---

## 🧠 Behavioral Patterns

1. 🧮 Strategy 

   Defines a family of algorithms.

   ```go
    package strategy
    
    type Strategy interface {
        Execute(a, b int) int
    }
    
    type Add struct{}
    func (Add) Execute(a, b int) int { 
        return a + b 
    }
    
    type Multiply struct{}
    func (Multiply) Execute(a, b int) int { 
        return a * b 
    }
    
    type Context struct {
        strategy Strategy
    }
    
    func (c *Context) SetStrategy(s Strategy) {
        c.strategy = s
    }
    
    func (c Context) ExecuteStrategy(a, b int) int {
        return c.strategy.Execute(a, b)
    }
   ```

1. 👀 Observer

   Notifies dependents of state changes.

   ```go
    package observer
    
    type Observer interface {
        Update(string)
    }
    
    type Subject interface {
        Attach(Observer)
        Notify()
    }
    
    type ConcreteSubject struct {
        observers []Observer
        state     string
    }
    
    func (s *ConcreteSubject) Attach(o Observer) {
        s.observers = append(s.observers, o)
    }
    
    func (s *ConcreteSubject) SetState(state string) {
        s.state = state
        s.Notify()
    }
    
    func (s *ConcreteSubject) Notify() {
        for _, o := range s.observers {
            o.Update(s.state)
        }
    }
    
    type ConcreteObserver struct {
        id string
    }
    
    func (o ConcreteObserver) Update(state string) {
        println("Observer", o.id, "received new state:", state)
    }
   ```

1. 🔁 State

   Allows an object to alter its behavior when its internal state changes.

   ```go
    package state
    
    type State interface {
        Handle() string
    }
    
    type Context struct {
        state State
    }
    
    func (c *Context) SetState(s State) {
        c.state = s
    }
    
    func (c Context) Request() string {
        return c.state.Handle()
    }
    
    type OnState struct{}
    func (OnState) Handle() string { 
        return "State is ON" 
    }
    
    type OffState struct{}
    func (OffState) Handle() string { 
        return "State is OFF" 
    }
   ```

---

## ✅ Conclusion

Design patterns are powerful tools in every Go developer’s toolkit. While Go encourages simplicity, these patterns still apply—especially in large-scale systems or when writing reusable libraries. Using patterns like Singleton, Adapter, and Strategy can lead to cleaner, more testable, and maintainable code.

Happy Go coding! 🐹
