use std::collections::HashMap;

fn make_orbit_map(input: &String) -> HashMap<&str, &str> {
    let mut relations: HashMap<&str, &str> = HashMap::new();

    for line in input.lines() {
        let mut test = line.split(")");
        let base = test.next().unwrap();
        let orbiter = test.next().unwrap();

        relations.insert(orbiter, base);
    }
    relations
}

pub fn part1(input: &str) -> String {
    let relations = make_orbit_map(input);

    let mut total_orbits = 0;
    for start in relations.keys() {
        total_orbits += 1;
        let mut next_step = relations.get(start).unwrap();

        while next_step != &"COM" {
            total_orbits += 1;
            next_step = relations.get(next_step).unwrap();
        }
    }
    assert!(total_orbits == 119831, "Should be 119831");
    total_orbits.to_string()
}

fn get_route_to_com(orbit_map: HashMap<&str, &str>, start: &str) -> Vec<String> {
    let mut steps: Vec<String> = Vec::new();
    let mut next_step = orbit_map.get(start).unwrap();

    while next_step != &"COM" {
        steps.push(next_step.to_string());
        next_step = orbit_map.get(next_step).unwrap();
    }
    steps
}

pub fn part2(input: &str) -> String {
    let relations = make_orbit_map(input);

    let you_path = get_route_to_com(relations.clone(), "YOU");
    let san_path = get_route_to_com(relations.clone(), "SAN");

    for (you_index, step) in you_path.iter().enumerate() {
        let result = match san_path.iter().position(|x| x == step) {
            Some(index) => (index + you_index).to_string(),
            None => continue,
        };

        assert!(result == "322", "Should be 322");
        return result;
    }
    panic!("Should have found a result!")
}
