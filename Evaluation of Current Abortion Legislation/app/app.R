#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    https://shiny.posit.co/
#
#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    https://shiny.posit.co/
#
knitr::opts_chunk$set(fig.width = 12, fig.height = 10)
library(shiny)
library(ggplot2)
library(tidyverse)
library(readxl)
library(readr)

#load ANES data on gender
abortion_gender <- read_excel("abortion_gender.xlsx")

# Define UI for application that draws a figure
ui <- fluidPage(
  
  # Application title
  titlePanel("Gendered Views on Abortion by State and Year"),
  
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel(
      selectInput("year",
                  "Year:",
                  choices = c(1984, 1986, 1988, 1990, 1992, 1994, 1996, 1998, 2000, 2004, 2008, 2012, 2016, 2020)),
      selectInput("state",
                  "State:", state.name)
    ),
    # Show a plot of the generated distribution
    mainPanel(
      plotOutput("gender_distplot", width = 1200, height = 800)
    )
  )
)

server <- function(input, output) {
  
  output$gender_distplot <- renderPlot({
    ggplot(
      filter(abortion_gender,year==input$year & state==input$state),
      aes(x=abort_num, y = freq, color=gender, fill=gender))+
      geom_bar(position = "dodge", stat= "identity", alpha=.5)+
      labs(x = "When Should Abortion be Legal?*", y = "", 
           caption = "*Plots display the difference in percentages for answers provided by male and female respondents to the question: \"By law, when should abortion be allowed?\"
      \nNever: Abortion should never be permitted, Rarely: The law should permit abortion only in certain cases (ie rape, incest), Sometimes: The law should permit\nabortion for other reasons but only after the need has been clearly established, Always: A woman should always be able to obtain an abortion
      \nNote: Distributions for states in years that had less than 10 respondents are not available
      \nData Source: ANES, American National Election Studies") +
      scale_x_discrete(breaks=c("1","2","3","4"),
                       labels=c("never", "rarely", "sometimes", "always")) +
      scale_y_continuous(labels = scales::percent) +
      scale_fill_manual(values=c("hotpink","blue"))+
      scale_color_manual(values=c("hotpink","blue"))+
      theme(axis.text.y=element_text(size=20),
            axis.text.x=element_text(size = 20),
            axis.title.x = element_text(size = 22),
            axis.title.y = element_text(size = 22),
            legend.text = element_text(size = 18),
            plot.caption = element_text(size = 12, hjust=0),
            legend.title = element_blank())
  })
}

# Run the application 
shinyApp(ui = ui, server = server)
