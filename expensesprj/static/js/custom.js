
function nameString(name){
    var b = "Sucks";
    var result = name +  b;
    return result;
}
console.log(nameString("Max "));


const sumOfTwoNumbers = (num1, num2) => {
    let sum = num1 + num2;
    return sum;
}
console.log(sumOfTwoNumbers(14,26));

//Recursion
var names = "robert";
function solutionRecurse(name){
    if (name.length === 0) return "";
    return name[name.length-1] + solutionRecurse(name.slice(0, name.length-1))
}
console.log(solutionRecurse(names));
function solutionRecurseNumbers(num1){
    if (num1 === 1) return 1;
    return num1 * solutionRecurseNumbers(num1 - 1)
}
console.log(solutionRecurseNumbers(5));