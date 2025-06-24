+++
date = '2025-06-24T12:00:00+02:00'
draft = false
title = 'The Generic Protocol Pattern in Go: Designing Extensible CLI Interfaces'
tags = ['go', 'golang', 'protocol', 'architecture', 'cli', 'design pattern']
categories = ['Programming', 'Go']
summary = 'Learn how to implement a flexible and extensible protocol pattern in Go for building structured CLI interfaces and stream-based IPC communication.'
comments = true
ShowToc = true
TocOpen = true
image = 'generic-protocol.jpg'
weight = 19
+++

![banner](banner.jpg)

In systems programming and CLI tool design, a consistent and extensible protocol can make or break maintainability. Whether you're building a REPL, a network service, or an internal CLI for scripting, the Generic Protocol Pattern helps you separate commands, parsers, and handlers.

This post introduces the pattern and demonstrates how to build a robust protocol interpreter in Go — one line at a time.
<div style="display: flex; justify-content: center;"> <img src="generic-protocol.jpg" alt="Generic Protocol Pattern in Go" style="max-width: 100%; height: auto;" /> </div>

---

## 🧩 What Is the Generic Protocol Pattern?

It’s a design pattern for stream-based command interpreters that:

- Accept string-based commands via stdin, socket, or pipe
- Parse input into structured messages
- Delegate logic to handlers
- Produce line-based responses

It's widely used in:

- Redis CLI protocol
- SMTP, FTP, and IMAP
- Debuggers and scripting engines
- REPLs and interactive shells

---

## 🧠 Go Interface Design

We define a generic Command interface:

```go
type Command interface {
    Name() string
}
```

And a Handler interface:

```go
type Handler interface {
    Handle(cmd Command) string
}
```

Then we use a Dispatcher to wire command names to handlers:

```go
type Dispatcher struct {
    handlers map[string]Handler
}

func (d *Dispatcher) Register(name string, handler Handler) {
    d.handlers[name] = handler
}

func (d *Dispatcher) Dispatch(cmd Command) string {
    h, ok := d.handlers[cmd.Name()]
    if !ok {
        return "ERR Unknown Command"
    }
    return h.Handle(cmd)
}
```

---

## 📦 Example Commands: LOAD, LOOKUP, EXIT

```go
type LoadCommand struct{}
func (LoadCommand) Name() string { return "LOAD" }

type LookupCommand struct {
    IP string
}
func (LookupCommand) Name() string { return "LOOKUP" }

type ExitCommand struct{}
func (ExitCommand) Name() string { return "EXIT" }
```

---

## 🗂 Command Parser

A simple parser can split input lines into command structs:

```go
func ParseCommand(line string) (Command, error) {
    parts := strings.Fields(line)
    if len(parts) == 0 {
        return nil, fmt.Errorf("empty input")
    }

    switch parts[0] {
    case "LOAD":
        return LoadCommand{}, nil
    case "LOOKUP":
        if len(parts) != 2 {
            return nil, fmt.Errorf("invalid LOOKUP args")
        }
        return LookupCommand{IP: parts[1]}, nil
    case "EXIT":
        return ExitCommand{}, nil
    default:
        return nil, fmt.Errorf("unknown command")
    }
}
```

---

## 🎮 Command Handlers

```go
type LoadHandler struct{}
func (h LoadHandler) Handle(cmd Command) string {
    // load logic
    return "OK"
}

type LookupHandler struct{}
func (h LookupHandler) Handle(cmd Command) string {
    ip := cmd.(LookupCommand).IP
    // resolve IP
    return "US,Hammond"
}

type ExitHandler struct{}
func (h ExitHandler) Handle(cmd Command) string {
    return "OK"
}
```

---

## 🔁 Main Loop

```go
func main() {
    dispatcher := Dispatcher{handlers: map[string]Handler{}}
    dispatcher.Register("LOAD", LoadHandler{})
    dispatcher.Register("LOOKUP", LookupHandler{})
    dispatcher.Register("EXIT", ExitHandler{})

    scanner := bufio.NewScanner(os.Stdin)
    for scanner.Scan() {
        input := scanner.Text()

        cmd, err := ParseCommand(input)
        if err != nil {
            fmt.Println("ERR")
            continue
        }

        result := dispatcher.Dispatch(cmd)
        fmt.Println(result)

        if cmd.Name() == "EXIT" {
            break
        }
    }
}
```

---

## ⚙️ Benefits of the Pattern

✅ Extensibility
New commands are easy to add — define a struct, implement a handler, register it.

✅ Separation of Concerns
Parsing, routing, and handling are cleanly isolated.

✅ Stream-Friendly
Ideal for REPLs, socket-based daemons, and interactive protocols.

✅ Testable
Handlers and parsers can be independently unit-tested.

---

## 📜 Conclusion

The Generic Protocol Pattern is an underappreciated gem in systems programming. Whether you're building an internal tool or network protocol, this approach provides a clean, extensible foundation with zero dependencies.

💡 Tip: Combine this with custom binary formats, caching, or memory pooling for serious performance wins.

---

🚀 Follow me on [norbix.dev](https://norbix.dev) for more insights on Go, system design, and engineering wisdom.
