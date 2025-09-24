+++
date = '2025-04-15T12:43:02+02:00'
draft = false
title = 'GoF Design Patterns in Go: Practical Examples'
tags = ['go', 'golang', 'design patterns', 'architecture']
categories = ['Programming', 'Go']
summary = 'Explore the 23 Gang of Four (GoF) design patterns in Go with clear explanations and code snippets, grouped into creational, structural, and behavioral categories.'
comments = true
ShowToc = true
TocOpen = true
image = 'banner.jpg'
weight = 5
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

   **Hint:** 

   Singleton quite often breaks the **Dependency Inversion Principle**!

   🧑‍💻 Example:

    ```go
    package singleton
    
    import (
        "sync"
    )
    
    var (
        instance *singleton
        // Ensures that a function is executed only once during the lifetime of a program, 
		// no matter how many times you call it, and no matter how many goroutines are calling it at the same time
        once     sync.Once
    )

    type singleton struct{
        Value string
    }
	
   func GetInstance(value string) *singleton {
    once.Do(func() {
        instance = &singleton{Value: value}
    })
    return instance
   }
    ```

   🧪 Usage

   ```go
   package main
   
   import (
   "fmt"
   "singleton"
   )
   
   func main() {
      a := singleton.GetInstance("First")
      b := singleton.GetInstance("Second")
      
      fmt.Println(a.Value) // Output: First
      fmt.Println(b.Value) // Output: First
	  
	  // Confirm both variables point to the same instance by using pointer equality. If they point to different objects, the comparison will return false.
	  fmt.Println(a == b) // Output: true
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

   🧑‍💻 Example:

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

   🧪 Usage
   
   ```go
   package main
   
   import (
   "fmt"
   "factory"
   )
   
   func main() {
       circle := factory.GetShape("circle")
       square := factory.GetShape("square")
   
       fmt.Println(circle.Draw()) // Output: Drawing Circle
       fmt.Println(square.Draw()) // Output: Drawing Square
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

   🧑‍💻 Example:

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

   🧪 Usage

   ```go
   package main
   
   import (
        "fmt"
        "builder"
   )
   
   func main() {
       car := builder.CarBuilder{}.
       SetEngine("V8").
       SetWheels(4).
       SetColor("Red").
       Build()
   
           fmt.Printf("%+v\n", car)
           // Output: {Engine:V8 Wheels:4 Color:Red}
   }
   ```

---

## 🧩 Structural Patterns

1.🔌 Adapter

   Allows incompatible interfaces to work together.

   An **Adapter** is a design construct that adapts an existing interface **SpecificRequest** to conform to the required interface **Request**. It acts as a translator or bridge between two systems that otherwise couldn’t work together.

   🧭 To implement an adapter in Go:

    - 🔍 Determine the **API you have** (e.g. `Adaptee`)
    - 🎯 Define the **API you need** (e.g. `Target`)
    - 🧩 Create an adapter struct that **aggregates** the adaptee (usually via a pointer)
    - ⚡ Optimize when needed — adapters may introduce intermediate representations, so use **caching** or other performance strategies as required

   This is especially useful when integrating legacy code or 3rd-party libraries into a new system with different interfaces.
    
   🧑‍💻 Example:  

   ```go
    package adapter
    
    type Target interface {
        Request() string
    }
    
    type Adaptee struct{}
    
    // Existing interface with a different method
    func (a Adaptee) SpecificRequest() string {
            return "Specific behavior"
    }
    
    type Adapter struct {
        Adaptee Adaptee
    }
    
	// Adapter implements the Target interface by translating the Request call to SpecificRequest
    func (a Adapter) Request() string {
        return a.Adaptee.SpecificRequest()
    }
   ```

   🧪 Usage

   ```go
   package main
   
   import (
       "fmt"
       "adapter"
   )
   
   func main() {
       adaptee := adapter.Adaptee{}
       adapterInstance := adapter.Adapter{Adaptee: adaptee}
   
       fmt.Println(adapterInstance.Request()) // Output: Specific behavior
   }
   ```

1. 🎀 Decorator

    Adds behavior to objects dynamically by **embedding** and extending existing functionality.

    The **Decorator pattern** is used when you want to:

    - ➕ **Augment** an object with additional behavior
    - 🚫 Avoid modifying existing code (✅ Open/Closed Principle — OCP)
    - 🧼 Keep new functionality **separate** and modular (✅ Single Responsibility Principle — SRP)
    - 🔄 Retain the ability to **interact with existing interfaces**

    The solution is to **embed** the decorated object and override or extend its behavior. This lets you build **stackable, reusable enhancements** without altering the base struct.

   🧑‍💻 Example: wrapping a basic `Coffee` with a `MilkDecorator`:

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

   🧪 Usage

   ```go
   package main
   
   import (
   "fmt"
   "decorator"
   )
   
   func main() {
       var coffee decorator.Coffee = decorator.SimpleCoffee{}
	   fmt.Println("Base cost:", coffee.Cost()) // Output: 2.0
   
       coffeeWithMilk := decorator.MilkDecorator{Coffee: coffee}
       fmt.Println("With milk:", coffeeWithMilk.Cost()) // Output: 2.5
   }
   ```

1. 🛡 Proxy (aka Virtual Proxy)

   Provides a surrogate or placeholder shows the “virtual proxy” pattern (lazy-loading the real object only when needed).

   How it works?
   
    - Image → the interface clients depend on (Display()).
   
    - RealImage → the heavy or expensive object to create.
   
    - ProxyImage → wraps RealImage and delays its creation until the first Display() call.
   
   This is a proxy because clients don’t know if they’re talking to RealImage or a ProxyImage.

   🧑‍💻 Example: 

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
            // Lazy initialization
            p.realImage = &RealImage{filename: p.filename}
        }
    
        return p.realImage.Display()
    }
   ```

   🧪 Usage

   ```go
   package main
   
   import (
       "fmt"
       "proxy"
   )
   
   func main() {
       img := &proxy.ProxyImage{filename: "cat.png"}
   
       // The real image is not loaded yet
       fmt.Println(img.Display()) // Output: Displaying cat.png
   
       // The real image is reused without reloading
       fmt.Println(img.Display()) // Output: Displaying cat.png
   }
   ```

1. 🌳 Composite

    Composes objects into tree structures.
    Composes objects into tree structures and lets you treat individual and composite objects uniformly.

    The Composite pattern is ideal when some components are single objects (like files), and others are containers of other components (like folders). Both should support a common interface so clients don’t need to differentiate between them.

    🧭 To implement a composite in Go:

    - 🧱 Define a common interface that all components implement.

    - 🌿 Implement Leaf objects (e.g. File, Button, TextField).

    - 🧺 Implement Composite objects (e.g. Folder, Panel) that aggregate children and delegate behavior to them.

    - 🔁 Add iteration if you need to traverse or walk the tree (e.g. using the Iterator pattern).

    This pattern shines when building hierarchical or nested structures such as UI components, file systems, or organization charts.

   🧑‍💻 Example:

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

    📦 Example usage:

    ```go
    func main() {
    file1 := Leaf{name: "FileA.txt"}
    file2 := Leaf{name: "FileB.txt"}
   
        folder := &Composite{}
        folder.Add(file1)
        folder.Add(file2)
   
        fmt.Println(folder.Operation()) // Output: FileA.txt FileB.txt
    }
    ```

    ✅ When to use Composite:
   
     - You want to treat individual and group objects the same way
     - You have recursive or nested structures
     - You want to delegate behavior to child components
   
    🔁 Bonus: Pair with the Iterator pattern to walk tree structures cleanly without exposing their internal representation.

---

## 🧠 Behavioral Patterns

1. 🧮 Strategy 

   Defines a family of algorithms.

   Encapsulates a family of algorithms and allows them to be selected and swapped at runtime.
   
   The Strategy pattern is used when you want to:
   
   - 🧠 Separate an algorithm into its skeleton and implementation steps
   - 🧩 Decompose behavior into high-level workflows and low-level operations
   - 🔄 Swap logic dynamically without changing the calling code
   - ✅ Adhere to the Open/Closed Principle (OCP) — new strategies without changing the high-level logic
   
   The solution is to define a high-level algorithm that delegates part of its logic to an injected strategy. This strategy follows a shared interface, so any implementation can be plugged in without breaking the algorithm.
   🍵 Analogy: making a hot beverage
   
   Many real-world algorithms follow this structure. Take making tea as an example:
   
       Skeleton algorithm:
       Boil water → Pour into cup → Add ingredient
   
       Concrete implementation:
       Add tea bag, coffee grounds, or cocoa powder
   
   The high-level process is reusable, and the final step is delegated to a drink-specific strategy. This is exactly how Strategy works.

   🧑‍💻 Example: Choosing an operation strategy 

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

   🧪 Usage

   ```go
   ctx := strategy.Context{}

   ctx.SetStrategy(strategy.Add{})
   fmt.Println(ctx.ExecuteStrategy(3, 4)) // Output: 7
   
   ctx.SetStrategy(strategy.Multiply{})
   fmt.Println(ctx.ExecuteStrategy(3, 4)) // Output: 12
   ```

   By:
   
   - Defining a common interface (Strategy)
   - Creating multiple concrete strategies (Add, Multiply)
   - Supporting runtime injection into a reusable context (Context)
   
   You separate the structure of the algorithm from its implementation. Just like boiling water and pouring it into a cup — what happens next depends on the drink you're making.
   
   This makes your code modular, extensible, and easy to adapt to new behaviors without touching your existing flow.

1. 👀 Observer

   Wants to listen to events and be notified when something happens.
   
   The Observer pattern is used when you want to:
   
   - 📣 Be informed when a particular object changes state, does something, or reacts to an external event
   - 👂 Let other objects (observers) subscribe to and react to those changes
   - 🔄 Decouple the source of truth from those reacting to it
   - ✅ Support dynamic subscription and unsubscription
   
   The solution is to have two participants:
   
   - 🟢 Observable: emits events and holds a list of observers
   - 🟡 Observer: subscribes and reacts to events
   
   When the observable changes, it notifies all observers — sending event data (commonly as interface{} in Go) to each subscriber. 
   This is an intrusive approach since the observable must provide explicit subscription management.

   🧑‍💻 Example:

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

   🧪 Usage
   
   ```go
   subject := &observer.ConcreteSubject{}
   
   observer1 := observer.ConcreteObserver{id: "A"}
   observer2 := observer.ConcreteObserver{id: "B"}
   
   subject.Attach(observer1)
   subject.Attach(observer2)
   
   subject.SetState("🚀 Launching")
   // Output:
   // Observer A received new state: 🚀 Launching
   // Observer B received new state: 🚀 Launching
   ```

   With Observer, you give objects the ability to react automatically to changes elsewhere, without tightly coupling them together. This pattern is especially helpful for:
   
   - UIs reacting to data changes
   - Logging and monitoring
   - Event-based systems
   
   **Hint:** 
   
   This approach is intrusive — the observable must explicitly support subscriptions and notify logic.

1. 🔁 State

   Allows an object to alter its behavior when its internal state changes — effectively changing its class at runtime.

   The State pattern is used when you want to:
   
   - 🔄 Let an object change behavior dynamically based on its current state
   - 📲 Model real-world systems where actions depend on state
   - 🧠 Manage complex state logic in a modular, maintainable way
   
   The solution is to encapsulate each state in its own type and let the context object delegate behavior to the current state. When the state changes, so does the object's behavior — without conditionals scattered throughout the code.

   These transitions are triggered by events (e.g. dialing, picking up, hanging up), and actions vary depending on the state. This is a perfect fit for a state machine — a formal model that defines:
   
   - 📥 Entry/exit actions for each state
   - 🔄 Transitions between states, often triggered by events
   - ✅ Guards that control whether a transition is allowed
   - ⚙️ A default behavior if no transition is found
   
   When systems grow in complexity, it pays to define states and transitions explicitly to keep logic clean and modular.

   🧑‍💻 Example:

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

   🧪 Usage

   ```go
   ctx := state.Context{}
   
   ctx.SetState(state.OnState{})
   fmt.Println(ctx.Request()) // Output: State is ON
   
   ctx.SetState(state.OffState{})
   fmt.Println(ctx.Request()) // Output: State is OFF
   ```
   
   With the State pattern:
   
   - You encapsulate each state and its logic in a separate type
   - The object transitions explicitly in response to triggers
   - Behavior is cleanly modular, without long chains of if or switch
   
   Whether you're modeling a telephone, a TCP connection, or a video player, state machines help you handle transitions with clarity, flexibility, and control.

---

## ✅ Conclusion

Design patterns are powerful tools in every Go developer’s toolkit. While Go encourages simplicity, these patterns still apply—especially in large-scale systems or when writing reusable libraries. Using patterns like Singleton, Adapter, and Strategy can lead to cleaner, more testable, and maintainable code.

Happy Go coding! 🐹

---

🚀 Follow me on [norbix.dev](https://norbix.dev) for more insights on Go, Python, AI, system design, and engineering wisdom.
