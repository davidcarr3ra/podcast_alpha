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

  const handleSendMessage = () => {
    if (inputMessage.trim() === "") return;

    const newMessages = [
      ...messages,
      { role: "user", content: inputMessage },
      { role: "assistant", content: "This is a sample response." },
    ];
    setMessages(newMessages);
    setInputMessage("");
  };

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="flex flex-col h-full">
		{/* <div className="flex flex-col bg-background"> */}
      {/* <header className="flex items-center justify-between p-4 border-b">
        <h1 className="font-heading text-2xl font-bold text-primary">DegenGPT</h1>
				<Button>Home</Button>
      </header> */}
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
          />
          <Button onClick={handleSendMessage}>
            <Send className="h-4 w-4" />
            <span className="sr-only">Send message</span>
          </Button>
        </div>
      </footer>
    </div>
  );
}