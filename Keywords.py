luck_keywords = [
    r"\b(luck|random|chance|alea|rolls?|dice|fortune|unpredictable)\b",
    r"\b(not in control|no control|out of control|beyond control)\b",
    r"\b(outcome|result|game\s*outcome) (is )?random\b"
]

bookkeeping_keywords = [
    r"\b(bookkeeping|record\s*(keeping|tracking)|data\s*tracking|data\s*recording|manual\s*entry)\b",
    r"\b(reference(s)?\s*(the\s*)?(rules?|rulebook|booklet|manual)|check(s|ing)?\s*(the\s*)?(rules?|rulebook|manual))\b",
    r"\b(rulebook|manual|booklet)\s*(is\s*(bad|awful|poor|terrible|confusing|hard\s*to\s*follow))\b",
    r"\b(update\s*(parameters|values|stats|numbers|scores|counters))\b",
    r"\b(manual\s*(calculation|tracking|entry|updating))\b",
    r"\b(continual\s*updating|frequent\s*updates|constant\s*adjustments)\b",
    r"\b(game\s*flow\s*interrupted|manual\s*data\s*entry|tracking\s*slows\s*down\s*gameplay)\b",
    r"\b(spending\s*too\s*much\s*time\s*tracking|having\s*to\s*write\s*down\s*data)\b",
    r"\b(feels\s*like\s*a\s*chore|unnecessary\s*steps|too\s*many\s*adjustments)\b",
    r"\b(not\s*engaging|adds\s*no\s*value|not\s*fun|tedious\s*task|boring\s*task)\b",
    r"\b(video\s*game\s*comparison|AI\s*does\s*this|should\s*be\s*automatic|automatically\s*calculated)\b",
    r"\b(prone\s*to\s*error|easy\s*to\s*make\s*mistakes|complicated\s*to\s*track)\b",
    r"\b(difficult\s*bookkeeping|hard\s*to\s*follow|leads\s*to\s*errors)\b",
    r"\b(rulebook\s*(is|was)?\s*(confusing|annoying|bad|poor|difficult|frustrating))\b",
    r"\b(checking\s*(rules?|rulebook|manual|instructions|guide)\s*(too\s*much|constantly|repeatedly))\b"
]


downtime_keywords = [
    r"\b(downtime|waiting\s*time|wait\s*time|idle\s*time|standby|lag\s*time)\b",
    r"\b(nothing (to )?do|bored|not engaged|no (thinking|strategy))\b",
    r"\b(turn\s*waiting|wait\s*for turn|unproductive)\b",
    r"\b(long (turn|pause|break|delay))\b",
    r"\b(boredom|time\s*wasting|waste (of )?time)\b"
]

interaction_keywords = [
    r"\b(interaction|interactivity|interact(s|ed|ing)?|player\s*interaction)\b",
    r"\b(player\s*influence|impact\s*other\s*players|mutual\s*influence)\b",
    r"\b(direct\s*interaction|affect\s*others|player\s*conflict)\b",
    r"\b(cross\s*play|opponent\s*interference|actions\s*impact\s*others)\b"
]

bash_leader_keywords = [
    r"\b(bash\s*(the\s*)?leader|target\s*leader|go\s*after\s*leader)\b",
    r"\b(prevent\s*leader\s*win|(block|stop|hinder)\s*leader)\b",
    r"\b(sacrifice\s*(myself|own advantage) (to|for) (stop|hinder|block))\b",
    r"\b(prevent victory|attack leader|hit\s*leader|stop\s*first\s*place)\b",
    r"\b(bash\s*(the\s*)?leader|attack\s*the\s*leader|target\s*leader)\b",
    r"\b(stop\s*leader|block\s*leader|hinder\s*leader|focus\s*on\s*leader)\b",
    r"\b(prevent\s*leader\s*win|prevent\s*the\s*leader\s*from\s*winning)\b",
    r"\b(sacrifice\s*(myself|advantage|turn)\s*to\s*(block|stop|hinder)\s*leader)\b",
    r"\b(no\s*gain\s*for\s*self|others\s*benefit\s*from\s*my\s*actions)\b",
    r"\b(taking\s*actions\s*against\s*the\s*leader\s*for\s*no\s*personal\s*gain)\b",
    r"\b(forced\s*to\s*attack\s*leader|must\s*stop\s*leader|mandatory\s*to\s*target\s*leader)\b",
    r"\b(spiacevole\s*situazione|costretto\s*a\s*fermare\s*il\s*leader)\b",
    r"\b(let\s*others\s*win|help\s*others\s*by\s*hitting\s*leader)\b",
    r"\b(all\s*against\s*the\s*leader|ganging\s*up\s*on\s*leader|leader\s*under\s*attack)\b",
    r"\b(leader\s*penalty|leader\s*punishment|hit\s*the\s*leader\s*mechanic)\b"
]

complicated_keywords = [
    r"\b(complicated|complex\s*rules|difficult\s*to\s*learn|hard\s*to\s*grasp)\b",
    r"\b(many\s*rules|lots\s*of\s*exceptions|too\s*many\s*variables)\b",
    r"\b(rule\s*exceptions|exception\s*to\s*rules|specific\s*rules)\b",
    r"\b(overly\s*complicated|difficult\s*to\s*understand|intricate)\b"
]

complex_keywords = [
    r"\b(complex|deep\s*strategy|hard\s*to\s*master|requires\s*skill)\b",
    r"\b(cause\s*more\s*problems|new\s*challenges|multiple\s*outcomes)\b",
    r"\b(requires\s*foresight|many\s*layers|difficult\s*to\s*anticipate)\b",
    r"\b(challenging\s*gameplay|strategic\s*depth|unpredictable\s*results)\b"
]


all_keywords = (
    luck_keywords + bookkeeping_keywords + downtime_keywords + 
    interaction_keywords + bash_leader_keywords + 
    complicated_keywords + complex_keywords
)