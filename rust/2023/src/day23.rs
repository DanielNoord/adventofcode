use std::collections::{HashMap, HashSet};

#[derive(Debug, PartialEq, Eq)]
enum Plot {
    Path,
    Forest,
    // The other Slopes don't occur in the test and final data
    SlopeRight,
    SlopeDown,
}

#[derive(Debug, PartialEq, Eq, Copy, Clone)]
enum Direction {
    Up,
    Right,
    Down,
    Left,
}

#[derive(Debug, Copy, Clone)]
struct Position {
    y: usize,
    x: usize,
    direction: Direction,
}

fn parse_map(input: &str) -> (HashMap<usize, HashMap<usize, Plot>>, usize, usize) {
    let mut final_map: HashMap<usize, HashMap<usize, Plot>> = HashMap::new();
    for (index, row) in input.lines().enumerate() {
        let row_entry = final_map.entry(index).or_default();
        for (x_index, plot) in row.char_indices() {
            let parsed_plot = match plot {
                '.' => Plot::Path,
                '#' => Plot::Forest,
                '>' => Plot::SlopeRight,
                'v' => Plot::SlopeDown,
                _ => panic!("Unsupported plot {}", plot),
            };
            row_entry.insert(x_index, parsed_plot);
        }
    }

    let max_y = final_map.len() - 1;
    let max_x = final_map.get(&0).unwrap().len() - 1;
    (final_map, max_y, max_x)
}

fn get_new_neighbours(
    position: &Position,
    max_y: usize,
    max_x: usize,
) -> Vec<Position> {
    // Create neighbours based on the current direction so we don't walk back over ourselves
    let mut neighbours: Vec<Position> = Vec::new();
    if position.y != usize::MIN && position.direction != Direction::Down {
        neighbours.push(Position {
            y: position.y - 1,
            x: position.x,
            direction: Direction::Up,
        })
    }
    if position.y != max_y && position.direction != Direction::Up {
        neighbours.push(Position {
            y: position.y + 1,
            x: position.x,
            direction: Direction::Down,
        })
    }
    if position.x != usize::MIN && position.direction != Direction::Right {
        neighbours.push(Position {
            y: position.y,
            x: position.x - 1,
            direction: Direction::Left,
        })
    }
    if position.x != max_x && position.direction != Direction::Left {
        neighbours.push(Position {
            y: position.y,
            x: position.x + 1,
            direction: Direction::Right,
        })
    }
    neighbours
}

fn walk_grid(
    grid: &HashMap<usize, HashMap<usize, Plot>>,
    position: &Position,
    max_y: usize,
    max_x: usize,
) -> Vec<Position> {
    let mut new_positions: Vec<Position> = Vec::new();

    for neighbour in get_new_neighbours(position, max_y, max_x) {
        let neighbour_plot = grid.get(&neighbour.y).unwrap().get(&neighbour.x).unwrap();

        match neighbour_plot {
            Plot::Forest => (),
            Plot::Path => new_positions.push(neighbour),
            Plot::SlopeDown => {
                // Check that we are not walking up the slope
                if neighbour.direction == Direction::Down {
                    new_positions.push(neighbour)
                }
            }
            Plot::SlopeRight => {
                // Check that we are not walking up the slope
                if neighbour.direction == Direction::Right {
                    new_positions.push(neighbour)
                }
            }
        }
    }

    new_positions
}

pub fn part1(input: &str) -> String {
    let (grid, max_y, max_x) = parse_map(input);

    let mut positions: Vec<(Position, u32)> = vec![(
        Position {
            y: 0,
            x: 1,
            direction: Direction::Down,
        },
        0,
    )];

    let mut options: Vec<u32> = Vec::new();

    while let Some((position, score)) = positions.pop() {
        for step in walk_grid(&grid, &position, max_y, max_x) {
            if step.y == max_y && step.x == max_x - 1 {
                options.push(score + 1);
                continue;
            }
            positions.push((step, score + 1))
        }
    }

    let result = options.iter().max().unwrap();

    // Should be 2386
    assert!(result == &2386, "Should be 2386");
    result.to_string()
}

pub fn part2(_input: &str) -> String {
    "".to_string()
}
