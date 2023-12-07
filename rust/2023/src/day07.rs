use std::{cmp::Ordering, collections::HashMap, str::FromStr};

#[derive(Debug, Eq, PartialEq, Hash, Clone, PartialOrd, Ord)]
enum CardValue {
    ONE,
    TWO,
    THREE,
    FOUR,
    FIVE,
    SIX,
    SEVEN,
    EIGHT,
    NINE,
    TEN,
    J,
    Q,
    K,
    A,
}

impl From<char> for CardValue {
    fn from(value: char) -> Self {
        match value {
            'A' => CardValue::A,
            'K' => CardValue::K,
            'Q' => CardValue::Q,
            'J' => CardValue::J,
            'T' => CardValue::TEN,
            '9' => CardValue::NINE,
            '8' => CardValue::EIGHT,
            '7' => CardValue::SEVEN,
            '6' => CardValue::SIX,
            '5' => CardValue::FIVE,
            '4' => CardValue::FOUR,
            '3' => CardValue::THREE,
            '2' => CardValue::TWO,
            '1' => CardValue::ONE,
            _ => panic!("Unexpected value {value}"),
        }
    }
}

#[derive(Debug, Clone)]
struct Hand {
    card_one: CardValue,
    card_two: CardValue,
    card_three: CardValue,
    card_four: CardValue,
    card_five: CardValue,
}

impl FromStr for Hand {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut numbers = s.chars();
        Ok(Hand {
            card_one: numbers.next().unwrap().try_into().unwrap(),
            card_two: numbers.next().unwrap().try_into().unwrap(),
            card_three: numbers.next().unwrap().try_into().unwrap(),
            card_four: numbers.next().unwrap().try_into().unwrap(),
            card_five: numbers.next().unwrap().try_into().unwrap(),
        })
    }
}

impl Hand {
    fn calculate_score(self: &Self) -> CardScore {
        let mut result: HashMap<CardValue, u32> = HashMap::new();
        for card in [
            &self.card_one,
            &self.card_two,
            &self.card_three,
            &self.card_four,
            &self.card_five,
        ] {
            *result.entry(card.clone()).or_insert(0) += 1;
        }
        let values = result.values();
        let values_count = values.len();
        match values.max().unwrap() {
            1 => CardScore::HighCard,
            2 => {
                if values_count == 3 {
                    CardScore::TwoPair
                } else {
                    CardScore::OnePair
                }
            }
            3 => {
                if values_count == 2 {
                    CardScore::FullHouse
                } else {
                    CardScore::ThreeOfAKind
                }
            }
            4 => CardScore::FourOfAKind,
            5 => CardScore::FiveOfAKind,
            _ => panic!("Can't have more than 5 cards, but we have"),
        }
    }

    fn calculate_score_part_two(self: &Self) -> CardScore {
        let mut result: HashMap<CardValue, u32> = HashMap::new();
        let scores = self.get_scores();
        let scotes_iter = scores.iter().filter(|x| x != &&CardValue::J);
        for card in scotes_iter {
            *result.entry(card.clone()).or_insert(0) += 1;
        }

        let mut sorted_count = Vec::from_iter(result.clone());
        sorted_count.sort_by(|a, b| b.1.cmp(&a.1));

        let values_count = sorted_count.len();
        if values_count == 0 {
            return CardScore::FiveOfAKind;
        }
        let jokers = self
            .get_scores()
            .iter()
            .filter(|x| x == &&CardValue::J)
            .count();

        let best_pair = &sorted_count[0];
        let mut score = match best_pair.1 {
            1 => CardScore::HighCard,
            2 => {
                if values_count > 1 && sorted_count[1].1 == 2 {
                    CardScore::TwoPair
                } else {
                    CardScore::OnePair
                }
            }
            3 => {
                if values_count > 1 && sorted_count[1].1 == 2 {
                    CardScore::FullHouse
                } else {
                    CardScore::ThreeOfAKind
                }
            }
            4 => CardScore::FourOfAKind,
            5 => CardScore::FiveOfAKind,
            _ => panic!("Can't have more than 5 cards, but we have"),
        };

        for _ in 0..jokers {
            score = score.upgrade();
        }

        score
    }

    fn get_scores(self: &Self) -> [CardValue; 5] {
        [
            self.card_one.clone(),
            self.card_two.clone(),
            self.card_three.clone(),
            self.card_four.clone(),
            self.card_five.clone(),
        ]
    }
}

#[derive(Debug, Eq, PartialEq, PartialOrd, Ord)]
enum CardScore {
    HighCard,
    OnePair,
    TwoPair,
    ThreeOfAKind,
    FullHouse,
    FourOfAKind,
    FiveOfAKind,
}

impl CardScore {
    fn upgrade(self: &Self) -> CardScore {
        match self {
            CardScore::HighCard => CardScore::OnePair,
            CardScore::OnePair => CardScore::ThreeOfAKind,
            CardScore::TwoPair => CardScore::FullHouse,
            CardScore::ThreeOfAKind => CardScore::FourOfAKind,
            CardScore::FullHouse => CardScore::FourOfAKind,
            CardScore::FourOfAKind => CardScore::FiveOfAKind,
            CardScore::FiveOfAKind => CardScore::FiveOfAKind,
        }
    }
}

fn compare_cards(value: &Hand, other: &Hand) -> Ordering {
    let own_score = value.calculate_score();
    let other_score = other.calculate_score();

    match own_score.cmp(&other_score) {
        Ordering::Greater => Ordering::Greater,
        Ordering::Less => Ordering::Less,
        Ordering::Equal => {
            for (card, other_card) in
                value.get_scores().iter().zip(other.get_scores().iter())
            {
                if card == other_card {
                    continue;
                }
                return card.cmp(other_card);
            }
            panic!("Should have returned")
        }
    }
}

fn compare_cards_part_two(value: &Hand, other: &Hand) -> Ordering {
    let own_score = value.calculate_score_part_two();
    let other_score = other.calculate_score_part_two();

    match own_score.cmp(&other_score) {
        Ordering::Greater => Ordering::Greater,
        Ordering::Less => Ordering::Less,
        Ordering::Equal => {
            for (card, other_card) in
                value.get_scores().iter().zip(other.get_scores().iter())
            {
                if card == other_card {
                    continue;
                }
                if card == &CardValue::J {
                    return Ordering::Less;
                } else if other_card == &CardValue::J {
                    return Ordering::Greater;
                }
                return card.cmp(other_card);
            }
            panic!("Should have returned")
        }
    }
}

pub fn part1(input: &String) -> String {
    let mut pairs = input
        .lines()
        .map(|x| x.split_at(5))
        .map(|x| (x.0.parse().unwrap(), x.1))
        .collect::<Vec<(Hand, &str)>>();
    pairs.sort_by(|a, b| compare_cards(&a.0, &b.0));
    let values: u32 = pairs
        .iter()
        .enumerate()
        .map(|x| {
            (x.0 + 1) as u32 * x.1 .1.strip_prefix(" ").unwrap().parse::<u32>().unwrap()
        })
        .sum();

    assert!(values == 250058342, "Should be 250058342");
    values.to_string()
}

pub fn part2(input: &String) -> String {
    let mut pairs = input
        .lines()
        .map(|x| x.split_at(5))
        .map(|x| (x.0.parse().unwrap(), x.1))
        .collect::<Vec<(Hand, &str)>>();
    pairs.sort_by(|a, b| compare_cards_part_two(&a.0, &b.0));
    let values: u32 = pairs
        .iter()
        .enumerate()
        .map(|x| {
            (x.0 + 1) as u32 * x.1 .1.strip_prefix(" ").unwrap().parse::<u32>().unwrap()
        })
        .sum();

    assert!(values == 250506580, "Should be 250506580 {values}");
    values.to_string()
}
