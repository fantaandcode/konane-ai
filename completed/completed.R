install.packages('plyr')
install.packages('dplyr')
install.packages('gridExtra')
install.packages(tidyverse)
library(plyr)
library(dplyr)
library(tidyverse)
library(grid)
library(gridExtra)

rd <- read.csv(file = 'run_data.csv')
td <- read.csv(file = 'turn_data.csv')

# make all NA to zero
rd[is.na(rd)] <- 0
td[is.na(td)] <- 0

color_win <- rd[1:2]
color_win <- count(color_win, 'fb_rem')
color_win$b_tot <- as.data.frame.matrix(t(table(rd[1:2])))$Black
color_win$w_tot <- as.data.frame.matrix(t(table(rd[1:2])))$White
color_win$b_wr <- color_win$b_tot / color_win$freq
color_win$w_wr <- color_win$w_tot / color_win$freq

# select only 
rd_turns <- rd[ ,!(colnames(rd) %in% c('win', 'fb_rem', 'tturn'))]
# get maxes of each turn's max number of choices
rd_turn_max <- apply(rd_turns, 1, max)
rd_turn_min <- apply(rd_turns, 1, min)

# basic histogram
hist(rd_turn_max, breaks = max(rd_turn_max))

rd_turn_avg <- colMeans(rd_turns, na.rm = TRUE)
colMax <- function(data) sapply(data, max, na.rm = TRUE)
rd_turn_max <- colMax(rd_turns)
colMin <- function(data) sapply(data, min, na.rm = TRUE)
rd_turn_min <- colMin(rd_turns)

# black and white turn separation
td_black <- td[which(td$turn %% 2 == 0),]
td_black$turn <- td_black$turn / 2 + 1  # normalize turns to 1, 2, 3, etc.
td_white <- td[which(td$turn %% 2 == 1),]
td_white$turn <- floor(td_white$turn / 2) + 1   # normalize like before
td_b_plot <- ggplot(td_black, aes(x=turn, y=moves)) + xlim(0, 150) + ylim(0, 100)
td_w_plot <- ggplot(td_white, aes(x=turn, y=moves)) + xlim(0, 150) + ylim(0, 100)

bt_plot <- td_b_plot + stat_density_2d(geom = "raster", aes(fill = stat(density)), contour = FALSE) + scale_fill_viridis_c()
wt_plot <- td_w_plot + stat_density_2d(geom = "raster", aes(fill = stat(density)), contour = FALSE) + scale_fill_viridis_c()

bt_full_plot = bt_plot + ggtitle("Available Black Moves") + theme(legend.position = "none")
wt_full_plot = wt_plot + ggtitle("Available White Moves") + theme(legend.position = "none")

grid.arrange(bt_full_plot, wt_full_plot, nrow=1)

