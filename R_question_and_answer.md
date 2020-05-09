## Concepts

**Q**: What and why is lazy evaluation? Give some use cases.

**A**: Lazy evaluation is a programming strategy that allows a symbol to be evaluated only when needed. It allows a program to be more efficient when used interactively: only the necessary symbols are evaluated and loaded in memory. https://www.r-bloggers.com/about-lazy-evaluation/

- Example 1: lazy evaluation allows unused arguments in a function.

  ```R
  aaa <- function(x, y, z){
      x + y
  }
  ```

- Example 2: But lazy evaluation also make things tricky. Check what happens when calling the following function.

  ```R
  # the function
  mean_of_that <- function(x, mean_of = mean(x)){
    # Of course I could use na.rm, it's an example ;)
    x <- x[!is.na(x)]
    print(x)
    cat("The mean of x is", mean_of)
  }
  
  # call the function, giving only one argument, x.
  # When mean_of is waked up in cat("The mean of x is", mean_of),
  # NA has been removed from x, so mean_of is the mean of
  # c(1, 2, 3, 4)
  mean_of_that(c(1,2,3,4,NA))
  ```




**Q**: What is lexical scoping?

**A**: Lexical scoping looks up name (variable or function) values based on how functions were nested when created, not how they are nested when they are called. 

- naming masking: If a name is not defined inside a function, R will look one level up from where the function is defined until global environment. Example:

  ```R
  x <- 1                # current environment
  h <- function(){
      y <- 2            # defined in h()
      i <- function(){
          z <- 3        # defined in i()
          c(x, y, z)
      }
      i()               # need three names, x, y, and z. z is defined in itself,
  }                     # y in function h and x in current environment
  h() 
  ```


- a fresh start: when a function is called, names defined inside this function does not stay in the environment.

  ```R
  j <- function(){
      if (!exists("a")){
          a <- 1
      } else {
          a <- a + 1
      }
      a
  }
  j()  # 1
  j()  # still 1
  a <- 10
  j()  # 11
  j()  # still 11
  ```




**Q**: Lexical scoping quiz: what is printed by code below?

```R
aaa <- function(){
    print(var1)
}

bbb <- function(){
    var1 <- 111
    aaa()
}

var1 <- 999
bbb()
```

**A**: It is 999 not 111, as `aaa()` is defined in the global environment. As `var1` is not defined inside `aaa()`, R will find its value one level up from where `aaa()` is defined, not from where `aaa()` is called.



## Data structures

### Atomic Vectors

**Q**: Is `c(1, c(2, 3), 4)` identical to `c(1, 2, 3, 4)`? How about `c(1, 2, 3)` and `1:3`?

**A**: Atomic vectors are created with `c()`, short for combine. Atomic vectors are always flat, that is, composite structures are removed. So   `c(1, c(2, 3), 4)` is actually identical to `c(1, 2, 3, 4)`. 

The relationship between `c(1, 2, 3)` is tricky: they are equal but not identical as they are of different data type.

```R
c(1, 2, 3) == 1:3
	# [1] TRUE TRUE TRUE

identical(c(1, 2, 3), 1:3)
	# FALSE

typeof(c(1, 2, 3))           # class(c(1, 2, 3)) is "numeric"
	# [1] "double"

typeof(1:3)                  # class(1:3) is "integer"
	# [1] "integer"
```



**Q**: What is coercion rule? What is the result of `c(TRUE, FALSE, 1, 2L, "a")`? How about `c(TRUE, FALSE, 1, 2L)`? 

**A**: The order of coercion is logical -> integer -> double (numeric) -> character. 

```R
c(TRUE, FALSE, 1, 2L, "a")  # character
	# [1] "TRUE"  "FALSE" "1"     "2"     "a"
c(TRUE, FALSE, 1, 2L)  # double
	# 1 0 1 2
```



**Q**: What is the results of `list(list(1, 2), c(3, 4))` and `c(list(1, 2), c(3, 4))`?

**A**: First of all, try to avoid them in your work; they are too confusing. With that said, the results are

```R
aaa = list(list(1, 2), c*3, 4)  # is a list of two elements: list(1, 2) and c(3, 4)
aaa[[1]]                        # this one is easy to understand
	# [[1]]
	# [1] 1

	# [[2]]
	# [1] 2
aaa[[2]]
	# [1] 3 4

bbb = c(list(1, 2), c(3, 4))  # is a list of four elements. how comes?
bbb                           # c() coerce c(3, 4) into a list and then combine
	# [[1]]                   # the two list into a big list.
	# [1] 1

	# [[2]]
	# [1] 2

	# [[3]]
	# [1] 3

	# [[4]]
	# [1] 4
```



**Q**: What is the result of `1 == "1"`? and why?

**A**: Surprisingly, `1 == "1"` is `TRUE`. The coercion rule dictates that the number `1` is coerced to character `"1"` automatically. So they are equal. For the same reason, `2 > "1"` , `TRUE > "a"`,  `FALSE > "a"`, and `3 < "a"` are `TRUE`. 

However, `NA > "a"` and  `NA > TRUE` are still `NA`. The `NA` will be coerced to the right data type but still `NA` of that type.



**Q**: What is the result of `c(1, 2) == list(1, 2)` and why?

**A**: The result is `TRUE, TRUE` . When `c()` and `list()` are in parallel, `c()` is coerced to `list()`. For example, `c(c(1, 2), list(3, 4))` becomes `c(list(1, 2), list(3, 4))`, which is `list(1, 2, 3, 4)`. 

 `c()` combines elements of all lists into one list. For example, `c(list(1, list(2, 3)), list(4, list(5, 6)))` equals to `list(1, list(2, 3), 4, list(5, 6))`. 





### subset_vector

**Q**: Given a vector `v = c(1, 4, 5, 9)`, how to get the subset of `c(4, 9)`?

**A**: Use the index of the two elements as `v[c(2, 4)]`. 

### subset_list

**Q**: Given a list `lst = list("a", 1:3, c(1, 4, 5, 9), LETTERS[1:3])` , how to get the `c(4, 9)` from the third list element?

**A**: Use `[[]]` to get the element of a list. The answer is `lst[[3]][c(2, 4)]`. 



## Base R functions

**Q**: How to use the `apply()` family functions? 

**A**: This family of functions apply a function on the elements of a vector, list, array, matrix, or data.frame and return a vector or list of the results. It works in the similar way as the `map()` function.

```R
# apply(X, margin, fun) specify an axis of a high dimensional data structure
df = data.frame(x = 1:3, y = 7:9)
apply(df, 1, sum)  # 1 row sum and 2 for column sum

# lapply(X, fun) and sapply(X, fun) on each element of a vector or list.
# data.frame is a list of columns
lapply(df, sum)  # column sum, sapply return a list, sapply a vector

# vapply(X, fun, FUN.VALUE) similar to sapply and lapply but must specify return type of fun(). In the example below, the return type of function x^2 is double(1)
vapply(1:3, function(x) x^2, FUN.VALUE = double(1))  # [1] 1 4 9

# mapply(fun, arg_1, arg_2, ...) supply vectors or lists to multiple argument of the function.
mapply(rep, 7:9, 1:3)  # return list(c(7), c(8, 8), c(9, 9, 9))
       
# tapply(X, groups, fun)  apply fun over X and return the results of each group. In the example below, group 'a' has values 1, 4, 7, 'b' 2, 5, 8, and 'c' 3, 6, 9. The mean of each group is 4, 5, and 6.
tapply(1:9, rep(c('a', 'b', 'c'), 3), mean)
	# a b c 
	# 4 5 6
```















## Popular packages

### `dplyr`

**Q**: How to use `dplyr::coalesce`?

**A**: Given a set of vectors of the same length, `coalesce()` finds the first non-missing value at each position.

```R
# example: a set of vectors x, y, z of the same length
x <- c("1", NA,  "3", NA,  NA)
y <- c(NA,  NA,  "c", "d", NA)
z <- c("A", "B", "C", "D", NA)

coalesce(x, y, z)
# [1] "1" "B" "3" "d" NA 
```

**Q**: How to use `dplyr:case_when()`?

**A**: `case_when` is an enhanced version of `ifelse`.

```R
# example
x = 1:7
case_when(x > 4 ~ "> 4",       # first assign value to this criteria
         x %% 2 == 0 ~ "mean", # asign value to the remaining 
         TRUE ~ "others")      # all remaining
# [1] "others" "mean"   "others" "mean"   "> 4"    "> 4"    "> 4"   
```

