#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(coinmarketcapr)
library(treemap)
library(plyr)
library(RJSONIO)
library(ECharts2Shiny)

#Import the market cap of all crypto
market_today <- get_marketcap_ticker_all()
df1 <- na.omit(market_today[,c('id','market_cap_usd')])
df1$market_cap_usd <- as.numeric(df1$market_cap_usd)
#Add the market price
#df1$formatted_market_cap <-  paste0(df1$id,'\n','$',format(df1$market_cap_usd,big.mark = ',',scientific = F, trim = T))

##Format the data to plot in a web application
colnames(df1) <- c("name", "value")

#To transform our dataframe in a list with two indexes to a list with
#the same number of indexes as the number of crypto
#see : https://stackoverflow.com/questions/18762229/convert-data-frame-to-json-in-this-format

make1 <- function(d){   
  list(
    name=d$name[1],
    value=d$value[1])
}

#This apply the function above to all elements and create the wanted list
L = dlply(df1,~name,make1)
names(L)=NULL

dat = toJSON(L, auto_unbox=TRUE)
#Reformat the annoying json to sui our needs
dat = gsub("\"name\"","name",dat)
dat = gsub("\"value\"","value",dat)
dat = gsub("\"","\'",dat)

# df1$formatted_market_cap <-  paste0(df1$id,'\n','$',format(df1$market_cap_usd,big.mark = ',',scientific = F, trim = T))
# crypto_map <- treemap(df1, index = 'formatted_market_cap', vSize = 'market_cap_usd', title = 'Cryptocurrency Market Cap', fontsize.labels=c(12, 8), palette='RdYlGn')
# crypto_map

# typeof(crypto_map)
# ui <- fluidPage(
#   d3tree2Output("au_crypto_map")
# )
# 
# typeof(crypto_map)
# server <- function(input,output){
#   output$au_crypto_map <- renderD3tree2({crypto_map})
# }
# 
# # Run the application
# shinyApp(ui = ui, server = server)

# Server function -------------------------------------------
server <- function(input, output) {
  # Call functions from ECharts2Shiny to render charts
  renderTreeMap(div_id = "test",
                data = dat)
}

# UI layout -------------------------------------------------
ui <- fluidPage(
  # We MUST load the ECharts javascript library in advance
  loadEChartsLibrary(),
  
  tags$div(id="test", style="width:100%;height:500px;"),
  deliverChart(div_id = "test")
)

# Run the application --------------------------------------
shinyApp(ui = ui, server = server)
