"use client";

import { useState, useEffect, useMemo } from 'react';
import { format } from 'date-fns';
import { Calendar as CalendarIcon } from 'lucide-react';
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

export default function DailySummary() {
  const [currentDate, setCurrentDate] = useState<Date>(new Date());
	const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [summary, setSummary] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentDate(new Date());
    }, 60000); // Update every minute
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (selectedDate) {
      fetchSummary(selectedDate);
    }
  }, [selectedDate]);

  const fetchSummary = async (date: Date) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch("http://127.0.0.1:8000/summarize_podcasts", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ date: format(date, 'yyyy-MM-dd') }),
      });

      const data = await response.json();
      if (data.error) {
        setError(data.error);
        setSummary("There was an error fetching the summary. Please try again.");
      } else {
        setSummary(data.summary);
      }
    } catch (error) {
      console.error("Error fetching summary:", error);
      setError("Failed to fetch summary. Please try again.");
      setSummary("There was an error fetching the summary. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const getTextContent = (selectedDate: Date | undefined) => {
    if (!selectedDate) {
      return {
        title: "Summary for " + format(currentDate, 'MMMM do, yyyy'),
        paragraph: summary
      };
    }

    const dayOfWeek = format(selectedDate, 'EEEE');
    const formattedDate = format(selectedDate, 'MMMM do, yyyy');

    return {
      title: `Summary for ${dayOfWeek}, ${formattedDate}`,
      paragraph: isLoading ? "Loading summary..." : (error || summary)
    };
  };

  const { title, paragraph } = useMemo(() => getTextContent(selectedDate), [selectedDate, summary, isLoading, error]);

  return (
    <section className="w-full max-w-4xl mx-auto p-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
        <div className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight">{title}</h2>
          <p className={cn(
            "text-muted-foreground",
            error && "text-red-500"
          )}>{paragraph}</p>
        </div>
        <div className="flex justify-center md:justify-end">
          <Popover>
            <PopoverTrigger asChild>
              <Button
                className={cn(
                  "w-[280px] justify-start text-left font-normal",
                  !selectedDate && "text-muted-foreground"
                )}
              >
                <CalendarIcon className="mr-2 h-4 w-4" />
                {selectedDate ? format(selectedDate, "PPP") : <span>Pick a date</span>}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0">
              <Calendar
                mode="single"
                selected={selectedDate}
                onSelect={(day: Date | undefined) => day && setSelectedDate(day)}
                initialFocus
              />
            </PopoverContent>
          </Popover>
        </div>
      </div>
    </section>
  );
}