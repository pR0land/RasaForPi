##### SAVE FACTORS #############################################################

medium_factor <- levels(sota$Medium)
complexity_factor <- levels(sota$Complexity)
incentive_types_factor <- levels(sota$`Incentive Type`)
time_of_payment_factor <- levels(sota$`Time of payment`)
prior_concent_factor <- levels(sota$Priorconcent)
save(medium_factor, complexity_factor, incentive_types_factor, time_of_payment_factor, prior_concent_factor, file = "factor_levels.Rdata")


##### LOAD AND FORMAT DATASET###################################################

  # 1. Click "SOTA Table (dots).csv" and click "Import Dataset".
  # 2. Set the "Delimiter" to "Semicolon".
  # 3. Click "Import".
  # Remember to "Set working directory" to the right folder. Then run this:
  # ( Mark it all and press CTRL+ENTER )

sota <- SOTA_Table_dots_
load("factor_levels.Rdata")
sota$Medium <- factor(SOTA_Table_dots_$Medium, levels = medium_factor)
sota$Complexity <- factor(SOTA_Table_dots_$Complexity, levels = complexity_factor)
sota$`Incentive Type` <- factor(SOTA_Table_dots_$`Incentive Type`, levels = incentive_types_factor)
sota$`Time of payment` <- factor(SOTA_Table_dots_$`Time of payment`, levels = time_of_payment_factor)
sota$Priorconcent <- factor(SOTA_Table_dots_$Priorconcent, levels = prior_concent_factor)

  # You dataset is now correctly formatted and called "sota".

################################################################################

library(ggplot2)
sota <- SOTA_Table_dots_
  # Swap out "Pages" with specific column
empty <- which(is.na(sota$Priorconcent))
sota <- sota[-empty, ]
ggplot(data = sota, aes(x = Priorconcent, y = RR)) +
  geom_boxplot() +
  #stat_summary(fun.y = "mean", geom = "line", aes(group = 1)) +
  labs(x = "Prior Knowledge", y = "Reponse Rate (%)")
my_agg <- data.frame(Group.1 = unique(sota$Priorconcent),
                     N = aggregate(sota$RR, by = list(sota$Priorconcent), FUN = length)[,2],
                     mean = aggregate(sota$RR, by = list(sota$Priorconcent), FUN = mean)[,2],
                     Mdn = aggregate(sota$RR, by = list(sota$Priorconcent), FUN = median)[,2],
                     sd = aggregate(sota$RR, by = list(sota$Priorconcent), FUN = sd)[,2])
my_agg$N <- sprintf("%.0f", my_agg$N)
my_agg$mean <- sprintf("%.1f", my_agg$mean)
my_agg$Mdn <- sprintf("%.1f", my_agg$Mdn)
my_agg$sd <- sprintf("%.1f", my_agg$sd)
my_agg


########## PRIKDIAGRAM ##########

  # omdøb "XXXX" i: x = XXXX, til den kolonne du gerne vil teste på
  # husk at importere "ggplot2" og at vinge den af i packages

ggplot(data = sota, aes(x = Items, y = RR)) +
  geom_point() +
  #stat_summary(fun.y = "mean", geom = "line", aes(group = 1)) +
  labs(x = "Items", y = "RR")
my_agg <- aggregate(sota$RR, by = list(sota$Items), FUN = function(x) c(mean = mean(x), sd = sd(x), N = length(x), Mdn = median(x)))
my_agg

########## BOKSPLOT ##########

  # omdøb "XXXX" i: x = XXXX, til den kolonne du gerne vil teste på
  # husk at importere "ggplot2" og at vinge den af i packages

ggplot(data = sota, aes(x = Priorconcent, y = RR)) +
  geom_boxplot() +
  stat_summary(fun.y = "mean", geom = "line", aes(group = 1)) +
  labs(x = "Priorconcent", y = "RR")