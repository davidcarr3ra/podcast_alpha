"use client"

import { useState } from 'react'
import { format } from 'date-fns'
import { Calendar as CalendarIcon } from 'lucide-react'
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"

export default function DailySummary() {
  const [date, setDate] = useState<Date>()

  const getTextContent = (selectedDate: Date | undefined) => {
    if (!selectedDate) {
      return {
        title: "Welcome!",
        paragraph: "Please select a date to see more information."
      }
    }

    const dayOfWeek = format(selectedDate, 'EEEE')
    const formattedDate = format(selectedDate, 'MMMM do, yyyy')

    return {
      title: `You selected ${dayOfWeek}`,
      paragraph: `The full date is ${formattedDate}. Each day is a new opportunity!`
    }
  }

  const { title, paragraph } = getTextContent(date)

  return (
    <section className="w-full max-w-4xl mx-auto p-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
        <div className="space-y-4">
          <h2 className="text-2xl font-bold tracking-tight">{title}</h2>
          <p className="text-muted-foreground">{paragraph}</p>
        </div>
        <div className="flex justify-center md:justify-end">
          <Popover>
            <PopoverTrigger asChild>
              <Button
                // variant={"outline"}
                className={cn(
                  "w-[280px] justify-start text-left font-normal",
                  !date && "text-muted-foreground"
                )}
              >
                <CalendarIcon className="mr-2 h-4 w-4" />
                {date ? format(date, "PPP") : <span>Pick a date</span>}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0">
              <Calendar
                mode="single"
                selected={date}
                onSelect={setDate}
                initialFocus
              />
            </PopoverContent>
          </Popover>
        </div>
      </div>
    </section>
  )
}