Scores = []
Grades=[]
class GradingSystem {
    // Method to determine the grade based on the score
    getGrade(score) {
    	let grade =''
        if (score >= 70 && score <= 100) {
        	grade = 'A'
        } else if (score >= 60 && score < 70) {
           grade = 'B';
        } else if (score >= 50 && score < 60) {
            grade = 'C';
        } else if (score >= 45 && score < 50) {
            grade = 'D';
        } else if (score >= 40 && score < 45) {
            grade = 'E';
        } else if (score >= 0 && score < 40) {
            grade = 'F';
        } else {
            return 'Invalid score';
        }
        Grades.push(grade)
        Scores.push(score)
    }
}

