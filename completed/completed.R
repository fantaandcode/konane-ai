install.packages('plyr')
library(plyr)

rd <- read.csv(file = 'run_data.csv')

# make all NA to zero
rd[is.na(rd)] <- 0

color_win <- rd[1:2]
color_win <- count(color_win, 'fb_rem')
color_win$b_tot <- as.data.frame.matrix(t(table(rd[1:2])))$Black
color_win$w_tot <- as.data.frame.matrix(t(table(rd[1:2])))$White
color_win$b_wr <- color_win$b_tot / color_win$freq
color_win$w_wr <- color_win$w_tot / color_win$freq

