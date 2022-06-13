# Decode simple captcha using Template Matching
## Process
```text
+-------+    +--------------+    +----------+    +--------+    +--------+
| input +--->| thresholding +--->| template +--->| select +--->| output |
+-------+    +--------------+    | matching |    +--------+    +--------+
                                 +----------+
                                      ^  
                                      |
                                 +----------+
                                 | table of |
                                 | symbols  |
                                 +----------+
``` 

## Example

### Input
![input](./assets/input.png)

### Thresholding
![thresholding](./assets/thresholding.png)

### Matches
![matches](./assets/matches.png)