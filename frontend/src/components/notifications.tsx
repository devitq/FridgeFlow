import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { IconBell, IconX, IconLoader2 } from '@tabler/icons-react'
import { motion, AnimatePresence } from 'framer-motion'
import { notificationsGet } from '@/api/v1/product/notifications'
import { delay } from '@/lib/delay'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Skeleton } from '@/components/ui/skeleton'

type Notification = {
  name: string
  level: string
  type: string
  timestamp: string
}

export function NotificationsPanel() {
  const [isOpen, setIsOpen] = useState(false)

  const {
    data: notifications,
    isLoading,
    isFetching,
    error,
  } = useQuery<Notification[]>({
    queryKey: ['notificationsGet'],
    queryFn: async () => {
      await delay(250)
      return await notificationsGet()
    },
    refetchInterval: 5000,
  })

  const getNotificationStyle = (level: string) => {
    switch (level) {
      case 'critical':
        return 'bg-red-100 border-red-300 dark:bg-red-900 dark:border-red-700'
      case 'high':
        return 'bg-yellow-100 border-yellow-300 dark:bg-yellow-900 dark:border-yellow-700'
      case 'average':
        return 'bg-green-100 border-green-300 dark:bg-green-900 dark:border-green-700'
      default:
        return 'bg-gray-100 border-gray-300 dark:bg-gray-800 dark:border-gray-600'
    }
  }

  const getNotificationText = (level: string) => {
    switch (level) {
      case 'critical':
        return 'истёк'
      case 'high':
        return 'истекает меньше чем через сутки'
      case 'average':
        return 'истекает в течение следующих трёх дней'
      default:
        return ''
    }
  }

  return (
    <>
      <Button
        variant='ghost'
        size='icon'
        className='relative scale-95 rounded-full'
        onClick={() => setIsOpen(true)}
      >
        <IconBell className='size-[1.2rem]' />
        {isLoading || isFetching ? (
          <IconLoader2 className='absolute -top-1 -right-1 size-4 animate-spin' />
        ) : notifications && notifications.length > 0 ? (
          <Badge
            variant='destructive'
            className='absolute -top-1 -right-1 px-1.5 py-0.5 text-xs'
          >
            {notifications.length}
          </Badge>
        ) : null}
        <span className='sr-only'>Уведомления</span>
      </Button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, x: 300 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 300 }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            className='fixed inset-y-0 right-0 z-50 w-80 bg-background shadow-lg'
          >
            <div className='flex items-center justify-between p-4 border-b'>
              <h2 className='text-lg font-semibold'>Уведомления</h2>
              <Button
                variant='ghost'
                size='icon'
                onClick={() => setIsOpen(false)}
              >
                <IconX className='size-4' />
              </Button>
            </div>
            <ScrollArea className='h-[calc(100vh-64px)]'>
              {isLoading || error ? (
                Array.from({ length: 3 }).map((_, index) => (
                  <Card key={index} className='m-2'>
                    <CardContent className='p-4'>
                      <Skeleton className='h-4 w-3/4 mb-2' />
                      <Skeleton className='h-3 w-full mb-2' />
                      <Skeleton className='h-3 w-1/2' />
                    </CardContent>
                  </Card>
                ))
              ) : notifications && notifications.length > 0 ? (
                notifications.map((notification, index) => (
                  <Card
                    key={index}
                    className={`m-2 border ${getNotificationStyle(notification.level)}`}
                  >
                    <CardContent className='p-4'>
                      <p className='mb-1'>
                        Продукт{' '}
                        <span className='font-bold'>{notification.name}</span>{' '}
                        {getNotificationText(notification.level)}
                      </p>
                      <p className='text-sm text-muted-foreground'>
                        {new Date(notification.timestamp).toLocaleDateString(
                          'ru-RU',
                          {
                            weekday: 'long',
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                          }
                        )}
                      </p>
                    </CardContent>
                  </Card>
                ))
              ) : (
                <p className='text-center text-muted-foreground p-4'>
                  Ничего не найдено
                </p>
              )}
            </ScrollArea>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
