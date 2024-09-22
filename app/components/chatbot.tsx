"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Bot, User, Send } from "lucide-react";

const initialMessages = [
  {
    role: "assistant",
    content: "Hello! How can I assist you today?",
  },
];

export default function Chatbot() {
  const [messages, setMessages] = useState(initialMessages);
  const [inputMessage, setInputMessage] = useState("");
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const [isLoading, setIsLoading] = useState(false);  // Added for loading state

  const handleSendMessage = async () => {
    if (inputMessage.trim() === "") return;

    // Optimistically update the messages to include the user's input
    const userMessage = { role: "user", content: inputMessage };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputMessage("");
    setIsLoading(true);

    try {
      // Send the user message to the FastAPI backend
      const response = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: inputMessage }),
      });

      const data = await response.json();

      // Add the assistant's response to the messages
      const assistantMessage = { role: "assistant", content: data.response };
      setMessages((prevMessages) => [...prevMessages, assistantMessage]);
    } catch (error) {
      console.error("Error fetching response:", error);
      const errorMessage = { role: "assistant", content: "Oops! Something went wrong. Please try again." };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="flex flex-col h-full">
      <ScrollArea className="flex-grow p-4" ref={scrollAreaRef}>
        {messages.map((message, index) => (
          <div key={index} className={`flex items-start mb-4 ${message.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`flex items-start max-w-[80%] ${message.role === "user" ? "flex-row-reverse" : "flex-row"}`}>
              <Avatar className={`${message.role === "user" ? "ml-2" : "mr-2"}`}>
                <AvatarImage src={message.role === "user" ? "/user-avatar.png" : "/ai-avatar.png"} />
                <AvatarFallback>{message.role === "user" ? <User /> : <Bot />}</AvatarFallback>
              </Avatar>
              <div className={`p-3 rounded-lg ${message.role === "user" ? "bg-primary text-primary-foreground" : "bg-secondary text-secondary-foreground"}`}>
                <p>{message.content}</p>
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex items-start mb-4 justify-start">
            <div className="flex items-start max-w-[80%] flex-row">
              <Avatar className="mr-2">
                <AvatarImage src="/ai-avatar.png" />
                <AvatarFallback><Bot /></AvatarFallback>
              </Avatar>
              <div className="p-3 rounded-lg bg-secondary text-secondary-foreground">
                <p>Typing...</p>
              </div>
            </div>
          </div>
        )}
      </ScrollArea>
      <footer className="p-4 border-t">
        <div className="flex items-center space-x-2">
          <Input
            type="text"
            placeholder="Type your message..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
            className="flex-grow"
            disabled={isLoading}  // Disable input while loading
          />
          <Button onClick={handleSendMessage} disabled={isLoading}>  {/* Disable button while loading */}
            <Send className="h-4 w-4" />
            <span className="sr-only">Send message</span>
          </Button>
        </div>
      </footer>
    </div>
  );
}
