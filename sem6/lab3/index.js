'use strict';

function* range(start = 0, end, step = 1) {

  for (let i = start; i < end; i+=step) {
    yield i;
  }
}


var data = 
{
	"L" : 10,
	"R" : 0.5,
	"Tos" : 300,
	"F0" : 100,
	"alpha0" : 1e-2,
	"alphaN" : 0.9e-2,
	"lambda0" : 0.1, // временно, пока не будет более точной инфы
	"lambdaN" : 0.2,
	"theta" : 293
	//"lambda0" : 0.15
};

function alpha(x) {
	let b = data.alphaN * data.L / (data.alphaN - data.alpha0);
	let a = -data.alpha0 * b;

	return a / (x - b);
}

function lamb(x) {
	let b = data.lambdaN * data.L / (data.lambdaN - data.lambda0);
	let a = -data.lambda0 * b;

	return a / (x - b);
}

function simpsonIntegration(a, b, n, func) {

    if (n < 1) {
        throw new Error('Неверное число интервалов в методе Симпсона');
    }	

    // console.log(func(0));

    let h = (b - a)/n;
    let res = 0;  

	for (let j of range(a+h/2, b, h)) {
        res += func(j-h/2) + 4*func(j) + func(j+h/2);
    }

    return h*res/6;
}


function u0(x) {
	let A = data.F0 / (2 * data.L * data.lambda0);

	return A * (x - data.L) * (x - data.L) + data.Tos;
}

function u1(x) {
	// return x * x * (x - data.L) * (x - data.L);
	return (x * x - data.L * data.L)**2; // 1
}

function u2(x) {
	// return x * x * x * (x - data.L) * (x - data.L);
	// return Math.pow(x,5) - 3*Math.pow(x,4)*data.L + 3*Math.pow(x,3)*data.L*data.L-x*x*data.L*data.L*data.L; // 1
	return x*x*(x*x - data.L*data.L)*(x*x - data.L*data.L);	
}

function u3(x) {
	return x * (x * x - data.L * data.L)**2;
	// return (x - data.L)*(x - data.L)*x**4; // 1
	// return (x * x - data.L * data.L)**2;
}

function u4(x) {
	return x*x*x*(x * x - data.L * data.L)**2;	
	// return x * x * (x - data.L) * (x - data.L);
}

// Первые производные функций U

function u0d1(x) {
	let A = data.F0 / (data.L * data.lambda0);
	return A * (x - data.L);
}

function u1d1(x) {
	// return 4 * Math.pow(x, 3) - 6 * x * x * data.L + 2 * x * data.L * data.L;
	return 4 * x**3 - 4 * x * data.L * data.L;
}

function u2d1(x) {
	// return 5 * Math.pow(x, 4) - 8 * Math.pow(x, 3) * data.L + 3 * x * x * data.L * data.L;
	// return 5*Math.pow(x,4)-12*Math.pow(x,3)*data.L+9*x*x*data.L*data.L-2*x*data.L*data.L*data.L; //норм
	return 6*x**5-8*data.L*data.L*x**3 + 2*x*data.L**4;
}

function u3d1(x) {
	return 5*x**4-6*x*x*data.L*data.L+data.L**4;
	// return 6*x**5 - 10*data.L*x**4+4*data.L*data.L*x**3;
	// return 4 * Math.pow(x, 3) - 6 * x * x * data.L + 2 * x * data.L * data.L;
}

function u4d1(x) {
	return 7*x**6 - 10*x**(4)*data.L**2 + 3*x*x*data.L**4;
	// return 4 * Math.pow(x, 3) - 6 * x * x * data.L + 2 * x * data.L * data.L;
}

// Вторые производные функций U

function u0d2(x) {
	return data.F0 / (data.L * data.lambda0);
}

function u1d2(x) {
	// return 12 * x * x - 12 * x * data.L + 2 * data.L * data.L;
	return 12*x*x - 4*data.L*data.L;
}

function u2d2(x) {
	// return 20 * Math.pow(x, 3) - 24 * x * x * data.L + 6 * x * data.L * data.L;
	// return 20*Math.pow(x,3)-36*x*x*data.L+18*x*data.L*data.L-6*data.L*data.L*data.L;
	return 30*x**4 - 24*x*x*data.L*data.L + 2*data.L**2;
}

function u3d2(x) {
	return 20*x**3 - 12*x*data.L*data.L;
	// return 30*x**4-40*data.L*x**3+12*data.L*data.L*x**2; 
	// return 12 * x * x - 12 * x * data.L + 2 * data.L * data.L;
}

function u4d2(x) {
	return 42*x**5 - 40*x*x*x*data.L**2 +6*x*data.L**4;
	// return 12 * x * x - 12 * x * data.L + 2 * data.L * data.L;
}

// Коэффициенты дифференциального оператора

function p(x) {	
	let b = data.lambdaN * data.L / (data.lambdaN - data.lambda0);
	return -1 / (x - b);	
}

function q(x) {
	return -2 * alpha(x) / (data.R * lamb(x));
}

function f(x) {
	return -2 * alpha(x) * data.Tos / (data.R * lamb(x));
}

// Применение дифференциального оператора к функции u(x) (возвращает функцию)

function Ldiff(u, ud1, ud2) {
	return function (x) { return ud2(x) + p(x) * ud1(x) + q(x) * u(x) };
}

// Расчет коэффициентов СЛАУ

function coef(ff, gg) {
	let integral = simpsonIntegration(0, 1, 15, x => ff(x)*gg(x));	
	return integral;		
}

function calcCoef(fs) {
	let c = [];
	for (let i = 0; i < fs.length; i++) {
		let row = [];
		for (let j = 0; j < fs.length; j++) {
			let a1 = coef(Ldiff(fs[j][0], fs[j][1], fs[j][2]), Ldiff(fs[i][0], fs[i][1], fs[i][2]));
			row.push(a1);
		}
		c.push(row);
	}


/*
	let a11 = coef(Ldiff(u1, u1d1, u1d2), Ldiff(u1, u1d1, u1d2));
	let a12 = coef(Ldiff(u2, u2d1, u2d2), Ldiff(u1, u1d1, u1d2));

	let a13 = coef(Ldiff(u3, u3d1, u3d2), Ldiff(u1, u1d1, u1d2));

	let a21 = coef(Ldiff(u1, u1d1, u1d2), Ldiff(u2, u2d1, u2d2));
	let a22 = coef(Ldiff(u2, u2d1, u2d2), Ldiff(u2, u2d1, u2d2));

	let a23 = coef(Ldiff(u3, u3d1, u3d2), Ldiff(u2, u2d1, u2d2));

	let a31 = coef(Ldiff(u1, u1d1, u1d2), Ldiff(u3, u3d1, u3d2));
	let a32 = coef(Ldiff(u2, u2d1, u2d2), Ldiff(u3, u3d1, u3d2));

	let a33 = coef(Ldiff(u3, u3d1, u3d2), Ldiff(u3, u3d1, u3d2));

	// return [[a11, a12],
			// [a21, a22]];
	return [[a11, a12, a13],
			[a21, a22, a23],
			[a31, a32, a33]];*/
	return c;
}

// Галеркин
function calcCoefColl(fs, x) {
	let c = [];
	for (let i = 0; i < x.length; i++) {
		let row = [];
		for (let j = 0; j < fs.length; j++) {
			let f = Ldiff(fs[j][0], fs[j][1], fs[j][2]);
			row.push(f(x[i]));
		}
		c.push(row);
	}

	return c;
}

// Столбец свободных членов

function calcB(fs) {
	let res = [];
	for (let i = 0; i < fs.length; i++) {
		let a = coef(function(x) { return f(x) - (u0d2(x) + p(x) * u0d1(x) + q(x) * u0(x)); }, Ldiff(fs[i][0], fs[i][1], fs[i][2]));
		res.push(a);
	}

	// let b1 = coef(function(x) { return f(x) - (u0d2(x) + p(x) * u0d1(x) + q(x) * u0(x)); }, Ldiff(u1, u1d1, u1d2));
	// let b2 = coef(function(x) { return f(x) - (u0d2(x) + p(x) * u0d1(x) + q(x) * u0(x)); }, Ldiff(u2, u2d1, u2d2));

	// let b3 = coef(function(x) { return f(x) - (u0d2(x) + p(x) * u0d1(x) + q(x) * u0(x)); }, Ldiff(u3, u3d1, u3d2));
	// let b4 = coef(function(x) { return f(x) - (u0d2(x) + p(x) * u0d1(x) + q(x) * u0(x)); }, Ldiff(u3, u3d1, u3d2));
	
	return res;
}

// Галеркин
function calcBColl(x) {
	let c = [];

	for (let i = 0; i < x.length; i++) {
		let a = f(x[i]) - (u0d2(x[i]) + p(x[i]) * u0d1(x[i]) + q(x[i]) * u0(x[i]));
		c.push(a);
	}

	return c;
}

function solveSLAU(A, B) {
	// Фукция решения СЛАУ с матрицей коэффициентов А и столбцом свободных членов В

	// Пока костыль
	let c2 = (A[0][0] * B[1] - A[1][0] * B[0]) / (A[0][0] * A[1][1] - A[1][0] * A[0][1]);
	let c1 = (B[0] - A[0][1] * c2) / A[0][0];

	return [c1, c2];
}


function gauss(mat, n) {  //int gauss(double **mat, double *result)	
    let rc = 0;
    let result = [];

    for (let i = 0; i < n && rc == 0; i++) {
        let max = i;

        for (let j = i; j < n; j++)
            if (mat[j][i]) {
                max = j;
                break;
            }

        if (max == n)
            throw new Error('Какая-то ошибка');
        else {
            let temp = mat[i];
            mat[i] = mat[max];
            mat[max] = temp;
        }

        for (let j = i + 1; j < n && rc == 0; j++) {
            for (let k = i + 1; k < n+1; k++)
                mat[j][k] -= mat[i][k] * (mat[j][i] / mat[i][i]);
            mat[j][i] = 0;
        }
    }

    for (let i = n - 1; i >= 0 && rc == 0; i--) {
        result[i] = mat[i][n];
        for (let j = i + 1; j < n; j++)
            result[i] -= mat[i][j] * result[j];
        result[i] /= mat[i][i];
    }

    return result;
}

function main() {

	let fs = [
			  [u1, u1d1, u1d2],
			  [u2, u2d1, u2d2],
			  [u3, u3d1, u3d2],
			  // [u4, u4d1, u4d2]
			  ];

	let A = calcCoefColl(fs, [2, 6, 8]);
	console.log(A);
	let B = calcBColl([2, 6, 8]);
	console.log(B);
	// let c = solveSLAU(A, B);
	// console.log(c);
	A[0][3] = B[0];
	A[1][3] = B[1];
	A[2][3] = B[2];
	// A[3][3] = B[3];
	console.log(A);
	// A[2][3] = B[2];
	// A[3][3] = B[3];
	let cc = gauss(A, fs.length);
	console.log(cc);	
	return function(x) { return u0(x) + cc[0] * u1(x) + cc[1] * u2(x) + cc[2] * u3(x); };
}

var d = [['x', 'T(x)']];
var func = main();
for (let i = 0; i <= data.L; i++) {
         d.push([i, func(i)]);
}

console.log(d);