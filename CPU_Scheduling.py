import copy

Path = "input/"
FileType = ".txt"
methods = ["FCFS", "RR", "SRTF", "PPRR", "HRRN", "All"]

class process():
    def __init__(self, id, cpu_burst, arrival_time, priority) -> None:
        self.ID = id
        self.CPU_Burst = cpu_burst
        self.Arrival_Time = arrival_time
        self.Priority = priority

        self.Complete_Time = 0
        self.Waiting_Time = 0
        self.Turnaround_Time = 0
        self.Last_CPU_Burst = cpu_burst
        self.Using_CPU_Time = 0
        self.Response_Ratio = (self.Waiting_Time+self.CPU_Burst)/self.CPU_Burst

        if ( id <= 16 ) : self.Gantt_ID = hex(id)[2:].upper()
        else: self.Gantt_ID = chr(id+55)

class FileIO():
    
    def __init__(self):
        pass

    def ReadFile(self, fileName):
        self.fileName = fileName

        processes = []
        with open( Path + fileName + FileType, mode="r" ) as File:
            method, timeSlice = [ int(token) for token in File.readline().split() ]
            Infomation = [ token for token in File.readline().split() ]
            line = File.readline().split()

            while line != []:
                one_process = process( int(line[0]), int(line[1]), int(line[2]), int(line[3]), )
                processes.append(one_process)
                line = File.readline().split()

        return method, timeSlice, processes

    def WriteFile(self, method, processes, ganttCharts):
        self.method = method
        self.Processes = processes
        self.GanttCharts = ganttCharts
        self.floor = 1
        if ( self.method == 5 ) : self.floor=5

        outputName = "out_" + self.fileName + FileType
        with open( outputName , mode="w" ) as File:

            # method Title
            if self.method == 3: File.write( "Priority RR\n" ) # PPRR CASE
            else : File.write( methods[self.method]+"\n") 

            self.Write_GanttChart(File)
            self.Write_Table_Format( File, "Waiting Time" )
            self.Write_Waiting_Time(File)
            self.Write_Table_Format( File, "Turnaround Time" )
            self.Write_Turnaround_Time(File)
            self.EndLine(File)

    def Write_GanttChart(self, File):

        # floor = 1
        # if ( self.method == 6 ) : floor=5
        
        for i in range(0,self.floor):
            File.write("==        ")
            if ( i == 1 ): File.write("  ") ## RR Case

            if ( self.floor == 1 ) :
                if ( self.method == 1 ): File.write("  ") ## RR Case
                File.write(methods[self.method]+"==\n")
            else: File.write(methods[i]+"==\n")

            File.write(self.GanttCharts[i])
            File.write("\n")
    
    def Write_Table_Format(self, File, WriteDataTitle):
        
        File.write("===========================================================\n\n")
        File.write( WriteDataTitle+"\n")
        File.write("ID")

        for i in range(0,self.floor):
            if ( self.floor == 1 ) : File.write("\t"+methods[self.method] )
            else: File.write("\t"+methods[i] )

        File.write("\n")
        File.write("===========================================================\n")
            
    def Write_Waiting_Time(self, File):

        for index in range(len(self.Processes[0])): # print waiting time
            File.write(str(self.Processes[0][index].ID))

            for i in range(0,self.floor):
                File.write("\t")
                File.write(str(self.Processes[i][index].Waiting_Time))

            File.write("\n")
            
    def Write_Turnaround_Time(self, File):

        for index in range(len(self.Processes[0])): # print turnaround time
            File.write(str(self.Processes[0][index].ID))

            for i in range(0,self.floor):
                File.write("\t")
                File.write(str(self.Processes[i][index].Turnaround_Time))

            File.write("\n")

    def EndLine(self, File):
        File.write("===========================================================\n\n")

def PrintData(processes):
    for process in processes:
        print( process.ID, '\t', process.CPU_Burst, '\t', process.Arrival_Time, '\t', process.Priority, '\t', process.Turnaround_Time )
    print()

''' CPU Scheduling '''
class CPU_Scheduling():
    def __init__(self, processes):
        self.Processes = processes
        self.Processes.sort( key=lambda process: (process.Arrival_Time, process.ID) ) # sort the process
        # PrintData( processes )

        self.Waiting_Queue = []
        self.Done_Processes = []
        self.Running_Process = None

        self.Current_Time = 0
        self.Processes_Quantity = len( processes )
        self.GanttChart = ""

    # default is arrival time first
    def Check_Waiting_Process(self):
        popIndex = 0
        for process in self.Processes:
            if ( process.Arrival_Time <= self.Current_Time ):
                self.Waiting_Queue.append( process )
                popIndex += 1
            else: break # TO CHECK
        
        if popIndex:
            self.PopOut_From_Processes(popIndex)
            return True
        else: return False
        
    def PopOut_From_Processes(self, index):
        for i in range(index):
            try:
                self.Processes.pop(0)
            except:
                pass

    def Estimate_Cost_Time(self):
        self.Running_Process.Complete_Time = self.Current_Time
        self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time # calculate the turnaround time
        self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst # calculate the waiting time

    def Dispatch2CPU(self):
        if len( self.Waiting_Queue ) > 0 :
            self.Running_Process = self.Waiting_Queue.pop(0)
            return True
        else: return False # if waiting Queue is empty

    def Check_Running_Process(self):
        if not self.Running_Process: # if CPU is edle
            return self.Dispatch2CPU()
        return True

    def Run_Process(self):
        
        self.Running_Process.Last_CPU_Burst -= 1
        #print( 'CPU Running || \t', self.Running_Process.ID, '\t', self.Running_Process.CPU_Burst, '\t', self.Running_Process.Gantt_ID ) # Check sceduling

        if ( self.Running_Process.Last_CPU_Burst == 0 ) :
            self.Estimate_Cost_Time()
            self.Done_Processes.append(self.Running_Process)
            self.Running_Process = None

    # def Draw_GanttChart(self):
    #     if self.Running_Process :
    #         self.GanttChart+=self.Running_Process.Gantt_ID
    #     else:
    #         self.GanttChart+='-'

    def Start(self):

        while len( self.Done_Processes ) < self.Processes_Quantity :
            # print( self.Current_Time )
            self.Check_Waiting_Process()
            self.Current_Time += 1

            if self.Check_Running_Process():
                self.GanttChart+=self.Running_Process.Gantt_ID # draw Gantt Chart
                self.Run_Process()
            else:
                self.GanttChart+='-' # draw Gantt Chart
        
        self.Done_Processes.sort( key=lambda process: process.ID )
        PrintData(self.Done_Processes)
        return self.Done_Processes

''' First Come First Service CPU Scheduling '''
class FCFS(CPU_Scheduling):
    def __init__(self, processes):
        super().__init__(processes)   

''' Run Robin CPU Scheduling '''
class RR(CPU_Scheduling):
    def __init__(self, processes, timeSlice ):
        super().__init__(processes)
        self.TimeSlice = timeSlice

    def Check_TimeOut(self): # check if running process is time out
        if self.Running_Process and self.Running_Process.Using_CPU_Time == self.TimeSlice:
            self.Running_Process.Using_CPU_Time = 0
            self.Waiting_Queue.append( self.Running_Process )
            self.Running_Process = None

    def Check_Running_Process(self):
        self.Check_TimeOut()
        return super().Check_Running_Process() # if CPU is IDLE, dispatch and return True, else return False

    def Run_Process(self):
        
        self.Running_Process.Last_CPU_Burst -= 1
        self.Running_Process.Using_CPU_Time += 1
        # print( 'CPU Running || \t', self.Running_Process.ID, '\t', self.Running_Process.CPU_Burst, '\t', self.Running_Process.Gantt_ID ) # Check sceduling

        if ( self.Running_Process.Last_CPU_Burst == 0 ) :
            self.Estimate_Cost_Time()
            self.Done_Processes.append(self.Running_Process)
            self.Running_Process = None
     
''' SRTF CPU Scheduling '''
class SRTF(CPU_Scheduling):

    def Check_Waiting_Process(self):
        super().Check_Waiting_Process()
        self.Waiting_Queue.sort( key=lambda process: (process.Last_CPU_Burst, process.Arrival_Time, process.ID) )

    def Check_Running_Process(self):
        if super().Check_Running_Process() :
            if len(self.Waiting_Queue) and self.Running_Process : self.Check_Content_Switch()
            return True
        return False

    def Check_Content_Switch(self):
        if self.Waiting_Queue[0].Last_CPU_Burst < self.Running_Process.Last_CPU_Burst:
            self.Waiting_Queue.append(self.Running_Process)
            self.Running_Process = self.Waiting_Queue.pop(0)
            self.Waiting_Queue.sort( key=lambda process: (process.Last_CPU_Burst, process.Arrival_Time, process.ID) )

''' PPRR CPU Scheduling '''
class PPRR(CPU_Scheduling):

    def __init__(self, processes, timeSlice ):
        super().__init__(processes)
        self.TimeSlice = timeSlice
        self.Same_Priority_Queue = []
        self.Current_Highest_Priority = 0

    def Check_Waiting_Process(self):
        super().Check_Waiting_Process() # Put Processes to waiting Queue
        if len(self.Waiting_Queue) > 1 :
            self.Waiting_Queue.sort( key=lambda process: (process.Priority) )

    def IsSamePriority(self):
        return self.Waiting_Queue[0].Priority == self.Current_Highest_Priority

    def PutIntoSamePriority2Queue(self):
        while len(self.Waiting_Queue) and self.IsSamePriority():
            # print( "put", self.Waiting_Queue[0].Gantt_ID ) # debug
            self.Same_Priority_Queue.append(self.Waiting_Queue.pop(0))

    def IsHigherPriority(self):
        if len(self.Waiting_Queue) == 0 : return False
        return ( self.Waiting_Queue[0].Priority < self.Current_Highest_Priority )
    
    def Preemptive(self):
        if len(self.Same_Priority_Queue) :
            for process in self.Same_Priority_Queue :
                self.Waiting_Queue.append( process )
            self.Same_Priority_Queue.clear()

        if self.Running_Process : 
            self.Running_Process.Using_CPU_Time = 0
            self.Waiting_Queue.append(self.Running_Process)
            self.Running_Process = None

    def Check_TimeOut(self): # check if running process is time out
        if self.Running_Process and self.Running_Process.Using_CPU_Time >= self.TimeSlice:
            self.Running_Process.Using_CPU_Time = 0
            self.Same_Priority_Queue.append( self.Running_Process )
            self.Running_Process = None

    def Check_Running_Process(self):
        if ( self.IsHigherPriority() ) : self.Preemptive() # if appear higher priority,then preemptive
        self.PutIntoSamePriority2Queue()
        if len(self.Same_Priority_Queue) > 0 : self.Check_TimeOut() # if there have two or more process in same priority
        
        # for process in self.Same_Priority_Queue: # debug
        #         print( 'Priority Queue : ', process.Gantt_ID ) # debug

        return super().Check_Running_Process() # Call Dispatch2CPU if cpu is idle

    def Dispatch2CPU(self): # if cpu is idle
        if len( self.Same_Priority_Queue ) > 0 : 
            self.Running_Process = self.Same_Priority_Queue.pop(0)
            return True

        elif len( self.Waiting_Queue ) > 0 :
            self.Running_Process = self.Waiting_Queue.pop(0)
            return True
        
        else: return False # if waiting Queue is empty

    def Run_Process(self):
            
        self.Running_Process.Last_CPU_Burst -= 1
        self.Running_Process.Using_CPU_Time += 1
        self.Current_Highest_Priority = self.Running_Process.Priority

        # print( 'CPU Running || \t', self.Running_Process.Priority, '\t', self.Running_Process.ID, '\t', self.Running_Process.Gantt_ID ) # Check sceduling
        # print( 'Priority Queue Size || \t', len(self.Same_Priority_Queue) )
        # print()

        if ( self.Running_Process.Last_CPU_Burst == 0 ) :
            self.Estimate_Cost_Time()
            self.Done_Processes.append(self.Running_Process)
            self.Running_Process = None

''' HRRN CPU Scheduling '''
class HRRN(CPU_Scheduling):

    def Check_Waiting_Process(self):
        super().Check_Waiting_Process()
        self.Waiting_Queue.sort( key=lambda process: (process.Response_Ratio, process.Arrival_Time, process.ID) )
        
        self.Update_Response_Ratio()

    def Update_Response_Ratio(self):
        if len( self.Waiting_Queue ) :
            for process in self.Waiting_Queue :
                process.Waiting_Time = self.Current_Time - process.Arrival_Time
                process.Response_Ratio = (process.Waiting_Time+process.CPU_Burst)/process.CPU_Burst
                # print( process.ID, '\t', process.Response_Ratio )

            self.Waiting_Queue.sort( reverse=True, key=lambda process: float(process.Response_Ratio) )
            self.Check_Same_Response_Ratio()
            

            # print( "Process Response Time" )
            # for process in self.Waiting_Queue :
            #     print( process.ID, '\t', process.Response_Ratio )

    def Check_Same_Response_Ratio(self):
        if len(self.Waiting_Queue) >= 2:
            if self.Waiting_Queue[0].Response_Ratio == self.Waiting_Queue[1].Response_Ratio:

                if self.Waiting_Queue[0].Arrival_Time > self.Waiting_Queue[1].Arrival_Time:
                    self.Waiting_Queue[0], self.Waiting_Queue[1] = self.Waiting_Queue[1], self.Waiting_Queue[0]
                    
                elif self.Waiting_Queue[0].Arrival_Time == self.Waiting_Queue[1].Arrival_Time:
                    if self.Waiting_Queue[0].ID > self.Waiting_Queue[1].ID:
                        self.Waiting_Queue[0], self.Waiting_Queue[1] = self.Waiting_Queue[1], self.Waiting_Queue[0]

    # def Dispatch2CPU(self):
    #     # self.Update_Response_Ratio()
    #     return super().Dispatch2CPU()

    # def Run_Process(self):
    #     # print( 'CPU Running || \t', self.Running_Process.Response_Ratio, '\t', self.Running_Process.ID, '\t', self.Running_Process.Gantt_ID ) # Check sceduling
    #     # print()
    #     return super().Run_Process()

def main():

    filename = input("Enter File Name: ")
    FIO = FileIO()

    try:
        method, timeSlice, processes = FIO.ReadFile(filename)
    except IOError:
        print( 'ERROR: can not found ' + filename + ' in input folder\n' )
    else:
        
        #PrintData(processes)
        All_Done_Processes = []
        All_GanttChart = []

        ### Method 1 FCFS
        if method == 1:
            print( "Running FCFS...\n" )

            FCFS_processes = copy.deepcopy(processes)
            FCFS_Simulation = FCFS( FCFS_processes )

            All_Done_Processes.append(FCFS_Simulation.Start())
            All_GanttChart.append(FCFS_Simulation.GanttChart)

            FIO.WriteFile( method=0, processes=All_Done_Processes, ganttCharts=All_GanttChart )
            print( "FCFS Completed !\n\n" )

        ### Method 2 RR
        elif method == 2: 
            
            print( "Running RR...\n" )

            RR_processes = copy.deepcopy(processes)
            RR_Simulation = RR( RR_processes, timeSlice )

            All_Done_Processes.append(RR_Simulation.Start())
            All_GanttChart.append(RR_Simulation.GanttChart)

            FIO.WriteFile( method=1, processes=All_Done_Processes, ganttCharts=All_GanttChart )
            print( "RR Completed !\n\n" )

        ### Method 3 SRTF
        elif method == 3: 
            
            print( "Running SRTF...\n" )

            SRTF_processes = copy.deepcopy(processes)
            SRTF_Simulation = SRTF( SRTF_processes )

            All_Done_Processes.append(SRTF_Simulation.Start())
            All_GanttChart.append(SRTF_Simulation.GanttChart)

            FIO.WriteFile( method=2, processes=All_Done_Processes, ganttCharts=All_GanttChart )
            print( "SRTF Completed !\n\n" )

        ### Method 4 PPRR
        elif method == 4: 
            
            print( "Running PPRR...\n" )

            PPRR_processes = copy.deepcopy(processes)
            PPRR_Simulation = PPRR( PPRR_processes, timeSlice )

            All_Done_Processes.append(PPRR_Simulation.Start())
            All_GanttChart.append(PPRR_Simulation.GanttChart)
            
            FIO.WriteFile( method=3, processes=All_Done_Processes, ganttCharts=All_GanttChart )
            print( "PPRR Completed !\n\n" )

        ### Method 5 HRRN
        elif method == 5: 
            
            print( "Running HRRN...\n" )

            HRRN_processes = copy.deepcopy(processes)
            HRRN_Simulation= HRRN( HRRN_processes )

            All_Done_Processes.append(HRRN_Simulation.Start())
            All_GanttChart.append(HRRN_Simulation.GanttChart)
            
            FIO.WriteFile( method=4, processes=All_Done_Processes, ganttCharts=All_GanttChart )
            print( "HRRN Completed !\n\n" )

        ### Method 6 ALL
        elif method == 6: 
            
            print( "Running ALL...\n" )
            

            ''' FCFS '''
            print( "FCFS" )
            FCFS_processes = copy.deepcopy(processes)
            FCFS_Simulation = FCFS( FCFS_processes )

            All_Done_Processes.append(FCFS_Simulation.Start())
            All_GanttChart.append(FCFS_Simulation.GanttChart)

            ''' RR '''
            print( "RR" )
            RR_processes = copy.deepcopy(processes)
            RR_Simulation = RR( RR_processes, timeSlice )

            All_Done_Processes.append(RR_Simulation.Start())
            All_GanttChart.append(RR_Simulation.GanttChart)

            ''' SRTF '''
            print( "SRTF" )
            SRTF_processes = copy.deepcopy(processes)
            SRTF_Simulation = SRTF( SRTF_processes )

            All_Done_Processes.append(SRTF_Simulation.Start())
            All_GanttChart.append(SRTF_Simulation.GanttChart)

            ''' PPRR '''
            print( "PPRR" )
            PPRR_processes = copy.deepcopy(processes)
            PPRR_Simulation = PPRR( PPRR_processes, timeSlice )

            All_Done_Processes.append(PPRR_Simulation.Start())
            All_GanttChart.append(PPRR_Simulation.GanttChart)

            ''' HRRN '''
            print( "HRRN" )
            HRRN_processes = copy.deepcopy(processes)
            HRRN_Simulation= HRRN( HRRN_processes )

            All_Done_Processes.append(HRRN_Simulation.Start())
            All_GanttChart.append(HRRN_Simulation.GanttChart)

            FIO.WriteFile( method=5, processes=All_Done_Processes, ganttCharts=All_GanttChart )

            print( "ALL Completed !\n\n" )
        
        else:
            print( "ERROR: the method doesn't exist\n" )
        
    print( "Program Exist...\n" )

if __name__ == '__main__':
    main()