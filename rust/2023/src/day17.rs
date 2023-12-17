use std::collections::{HashMap, HashSet};

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
struct Node {
    y: usize,
    x: usize,
}

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
enum Direction {
    Up,
    Right,
    Down,
    Left,
    // This represents the starting position
    None,
}

fn make_grid(input: &str) -> (HashMap<Node, u32>, usize, usize) {
    // Turn the input into a graph with the cost per node as well as calculate the max indices
    let mut grid: HashMap<Node, u32> = HashMap::new();
    let mut max_y = usize::MIN;
    let mut max_x = usize::MIN;

    for (y_index, row) in input.lines().enumerate() {
        max_y = y_index;
        for (x_index, value) in row.char_indices() {
            grid.insert(
                Node {
                    y: y_index,
                    x: x_index,
                },
                value.to_digit(10).unwrap(),
            );
            max_x = x_index;
        }
    }
    (grid, max_y, max_x)
}

impl Node {
    fn get_neighbours(
        self,
        grid: &HashMap<Node, u32>,
        direction: Direction,
        max_y: usize,
        max_x: usize,
        min_steps: usize,
        max_steps: usize,
    ) -> Vec<(Node, u32, Direction)> {
        let mut neighbours: Vec<(Node, u32, Direction)> = Vec::new();
        match direction {
            Direction::None => {
                let mut cost: u32 = 0;
                for step in 1..max_steps + 1 {
                    if self.y + step <= max_y {
                        let node = Node {
                            y: self.y + step,
                            x: self.x,
                        };
                        cost += grid.get(&node).unwrap();
                        if step >= min_steps {
                            neighbours.push((node, cost, Direction::Down))
                        }
                    }
                }

                let mut cost: u32 = 0;
                for step in 1..max_steps + 1 {
                    if self.x + step <= max_x {
                        let node = Node {
                            y: self.y,
                            x: self.x + step,
                        };
                        cost += grid.get(&node).unwrap();
                        if step >= min_steps {
                            neighbours.push((node, cost, Direction::Right))
                        }
                    }
                }
            }
            Direction::Right | Direction::Left => {
                let mut cost: u32 = 0;
                for step in 1..max_steps + 1 {
                    if self.y >= usize::MIN + step {
                        let node = Node {
                            y: self.y - step,
                            x: self.x,
                        };
                        cost += grid.get(&node).unwrap();
                        if step >= min_steps {
                            neighbours.push((node, cost, Direction::Up))
                        }
                    }
                }

                let mut cost: u32 = 0;
                for step in 1..max_steps + 1 {
                    if self.y + step <= max_y {
                        let node = Node {
                            y: self.y + step,
                            x: self.x,
                        };
                        cost += grid.get(&node).unwrap();

                        if step >= min_steps {
                            neighbours.push((node, cost, Direction::Down))
                        }
                    }
                }
            }
            Direction::Down | Direction::Up => {
                let mut cost: u32 = 0;
                for step in 1..max_steps + 1 {
                    if self.x >= usize::MIN + step {
                        let node = Node {
                            y: self.y,
                            x: self.x - step,
                        };
                        cost += grid.get(&node).unwrap();

                        if step >= min_steps {
                            neighbours.push((node, cost, Direction::Left))
                        }
                    }
                }

                let mut cost: u32 = 0;
                for step in 1..max_steps + 1 {
                    if self.x + step <= max_x {
                        let node = Node {
                            y: self.y,
                            x: self.x + step,
                        };
                        cost += grid.get(&node).unwrap();

                        if step >= min_steps {
                            neighbours.push((node, cost, Direction::Right))
                        }
                    }
                }
            }
        }
        neighbours
    }
}

fn dijkstra(
    grid: HashMap<Node, u32>,
    max_y: usize,
    max_x: usize,
    min_steps: usize,
    max_steps: usize,
) -> u32 {
    let destination: Node = Node { y: max_y, x: max_x };
    let start: (Node, Direction) = (Node { y: 0, x: 0 }, Direction::None);

    let mut visited: HashSet<(Node, Direction)> = HashSet::new();
    let mut costs: HashMap<(Node, Direction), u32> = HashMap::new();

    // This should be a BinaryHeap but I have no clue how to do the comparison on only the first
    // element
    let mut queue: Vec<(u32, (Node, Direction))> = vec![(0, start)];

    while let Some((total_cost, path)) = queue.pop() {
        // Stop if we're done
        if path.0 == destination {
            return total_cost;
        }

        // Skip if already visited
        if visited.contains(&path) {
            continue;
        }

        // Mark visited, even though we don't have costs yet
        visited.insert(path);

        for (neighbour_node, weight, new_direction) in path
            .0
            .get_neighbours(&grid, path.1, max_y, max_x, min_steps, max_steps)
        {
            let mut move_cost = total_cost + weight;

            let prev_cost = costs.entry((neighbour_node, new_direction)).or_insert(0);
            if prev_cost > &mut move_cost || prev_cost == &0 {
                *costs.get_mut(&(neighbour_node, new_direction)).unwrap() = move_cost;
                queue.push((move_cost, (neighbour_node, new_direction)));
            }
        }

        queue.sort_by(|a, b| b.0.cmp(&a.0));
    }

    panic!("Should have found a solution!")
}

pub fn part1(input: &str) -> String {
    let (grid, max_y, max_x) = make_grid(input);
    let result = dijkstra(grid, max_y, max_x, 0, 3);

    assert!(result == 742, "Should be 742");
    result.to_string()
}

pub fn part2(input: &str) -> String {
    let (grid, max_y, max_x) = make_grid(input);
    let result = dijkstra(grid, max_y, max_x, 4, 10);

    assert!(result == 918, "Should be 918");
    result.to_string()
}
