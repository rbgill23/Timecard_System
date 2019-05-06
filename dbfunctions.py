import mysql.connector as mariadb

class TimeCardDB(object):
	def __init__(self):
		try:
			self.connect = mariadb.connect(user='gfptime', password='time1923', database='TimeCards')
			self.cursor = self.connect.cursor()
		except:
			try:
				self.connect = mariadb.connect(host='192.168.1.114',port ='3306', user='rbg', password='time1923', database='TimeCards')
				self.cursor = self.connect.cursor()
			except:
				try:
					self.connect = mariadb.connect(host='192.168.1.114',port ='3306', user='rbgSurface', password='time1923', database='TimeCards')
					self.cursor = self.connect.cursor()

				except mariadb.Error as error:
					print("Error: {}".format(error))
		#~ return self.connect
		
	def listActiveEmployees(self):
		try:
			qry = "SELECT * FROM Employees WHERE `Terminated` = 'NO' ORDER BY LastName ASC, FirstName ASC"
			self.cursor.execute(qry)
			#print("ID\tLast\t   First    Middle")
			
			cboxvalue = []
			for row in self.cursor.fetchall():
				cv = row[3]+' '+ row[1]+' '+ row[2]
				cboxvalue.append(cv)
			return cboxvalue
		except mariadb.Error as error:
			self.connect.rollback()
			print("Error: {}".format(error))

	def listTermEmployees(self):
		try:
			qry = "SELECT * FROM Employees WHERE `Terminated` = 'YES' ORDER BY LastName ASC, FirstName ASC"
			self.cursor.execute(qry)
			#print("ID\tLast\t   First    Middle")
			
			cboxvalue = []
			for row in self.cursor.fetchall():
				cv = row[3]+' '+ row[1]+' '+ row[2]
				cboxvalue.append(cv)
			return cboxvalue
		except mariadb.Error as error:
			self.connect.rollback()
			print("Error: {}".format(error))
			
	def newemployee(self, firstname, middleinitial, lastname):
		
		try:
			query = 'INSERT INTO Employees (FirstName,MiddleInitial,LastName,`Terminated`) VALUES (%s,%s,%s,%s)'
			val = (firstname, middleinitial ,lastname, 'NO')
			self.cursor.execute(query,val)
		except mariadb.Error as error:
			print("Error: {}".format(error))
		self.connect.commit()
		
		try:
			query = 'CREATE TABLE {table} (ID INT AUTO_INCREMENT PRIMARY KEY, TimeStampIN	DATETIME,\
			TimeStampOUT DATETIME,Date DATE, TimeIN TIME, TimeOUT TIME, TimeTOTAL DECIMAL, OT DECIMAL, Tent DECIMAL,\
			TentAttendent DECIMAL, Holiday DECIMAL, Vacation DECIMAL, LowEarnings DECIMAL, OFF CHAR(4))'
			dbName = firstname + '_' + middleinitial + '_' + lastname
			self.cursor.execute(query.format(table=dbName))
		except mariadb.Error as error:
			print("Error: {}".format(error))
		self.connect.commit() 
	
	def editEmployee(self, firstname, middleinitial, lastname, firstEdit, middleEdit, lastEdit, termEdit):
		try:
			qry = "UPDATE Employees SET FirstName = %s, MiddleInitial = %s, LastName = %s, `Terminated` = %s WHERE FirstName = %s AND MiddleInitial = %s AND LastName = %s"
			val = (firstEdit,middleEdit, lastEdit, termEdit, firstname, middleinitial, lastname)
			self.cursor.execute(qry,val)
		except mariadb.Error as error:
			print("Error: {}".format(error))
		self.connect.commit()
	def dbclose(self):
		try:
			#print('close')
			self.connect.close()
		except mariadb.Error as error:
			print("Error: {}".format(error))
	def pullTimeRecord(self, fullname, date):
		try:
			qry = "SELECT * FROM " + fullname + " WHERE Date = " + date
			self.cursor.execute(qry)
			records = self.cursor.fetchone()
			if records == None:
				return records
			else:
				return self.cursor.fetchall()
			
		except mariadb.Error as error:
			print("Error: {}".format(error))

if __name__ == '__main__':
	db=TimeCardDB()
	db.pullTimeRecord('Russell_B_Gillespie',"'2019-05-03'")
	db.dbclose()
